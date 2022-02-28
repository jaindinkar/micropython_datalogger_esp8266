import os
from time import sleep, sleep_ms
from machine import Pin, I2C, SPI
from onewire import OneWire
# import micropython

from ds18x20 import DS18X20
from ssd1306 import SSD1306_I2C
from libs.bme280_sm import BME280
from libs.scd30_sm import SCD30
from libs.sdcard import SDCard

import modules.net_connect as net_connect


# Pin Assignment
p_i2c_sda = Pin(4) # D2
p_i2c_scl = Pin(5) # D1
p_hspi_en = Pin(15) # D8
p_one_wire = Pin(0) # D3 Flash button might not work. 
# SPI will take GPIO 12,13,14 | D6,D7,D5 automatically.

# ESP8266 I2C Pin assignment
i2c = I2C(scl=p_i2c_scl, sda=p_i2c_sda)
# ESP8266 One Wire Pin assignment
one_wire = OneWire(p_one_wire)
# ESP8266 SPI Pin assignment
hspi = SPI(1)


# Availablity check:
is_available_ds18 = False
is_available_bme280 = False
is_available_ssd1306 = False
is_available_scd30 = False
is_available_sd = False


print()  # First space for terminal print.

# SPI sd card config:
try:
  os.umount('/sdmc')
  print('Unmounted old SD card on /sdmc path.')
except BaseException as e:
  print(f"No previous SD card mount point found. Error: {e}")

# print(micropython.mem_info(1))
try:
  sd = SDCard(hspi, p_hspi_en)
  print('Found SD card.')
  vfs = os.VfsFat(sd)
  print('SD card VfsFat obj created.')
  os.mount(vfs, '/sdmc')
  # os.mount(sd, '/sdmc')
  print(os.listdir("/sdmc"))
  os.umount('/sdmc')
  print('Mounted SD card on /sdmc path.')
  is_available_sd = True
except BaseException as e:
  print(f"SD card error. Error: {e}")


# Print available I2C devices:
# print(f"Available I2C addresses: {list(map(hex, i2c.scan()))}")

# One-wire DS18B20 config:
try:
  ds_sensor = DS18X20(one_wire)
  roms = ds_sensor.scan()
  if len(roms):
    print('Found DS devices: ', roms)
    is_available_ds18 = True
  else:
    print('No DS18B sensor present on assigned pin.')
except BaseException as e:
  print(f"Could not found any DS18B sensor on assigned pin. Error: {e}")

# I2C OLED Config:
sleep_ms(300)
try:
  oled_width = 128
  oled_height = 64
  oled = SSD1306_I2C(oled_width, oled_height, i2c)
  print('Found SSD 1306 OLED Display.')
  is_available_ssd1306 = True
except BaseException as e:
  print(f'Could not found any SSD1306 OLED on I2C bus. Error: {e}')

# I2C BME280 Config:
sleep_ms(500)
try:
  bme = BME280(i2c=i2c)
  print('Found BME 280 Sensor.')
  is_available_bme280 = True
except BaseException as e:
  print(f'Could not found any BME280 Sensor on I2C bus. Error: {e}')

# I2C SCD30 Config:
sleep_ms(500)
try:
  scd30 = SCD30(i2c, 0x61)
  print('Found SCD30 Sensor.')
  is_available_scd30 = True
except BaseException as e:
  print(f'Could not found any SCD30 Sensor on I2C bus. Error: {e}')


# Function for updating OLED Screen
def updateScreen(
  str_humi_bme280='N/A',
  str_temp_bme280='N/A',
  str_pres_bme280='N/A',
  str_temp_ds18='N/A',
  str_humi_scd30='N/A',
  str_temp_scd30='N/A',
  str_co2_scd30='N/A'
):
  # Unit constants
  unit_humi = '%RH'
  unit_temp = 'degC'
  unit_pres = 'mBar'
  unit_co2 = 'ppm'

  oled.fill(0)
  oled.text(
      f"BH-{'N/A' if str_humi_bme280 is None else str_humi_bme280} {unit_humi}", 0, 0)
  oled.text(
      f"BT-{'N/A' if str_temp_bme280 is None else str_temp_bme280} {unit_temp}", 0, 10)
  oled.text(
      f"BP-{'N/A' if str_pres_bme280 is None else str_pres_bme280} {unit_pres}", 0, 20)

  oled.text(
      f"SH-{'N/A' if str_humi_scd30 is None else str_humi_scd30} {unit_humi}", 0, 35)
  oled.text(
      f"ST-{'N/A' if str_temp_scd30 is None else str_temp_scd30} {unit_temp}", 0, 45)
  oled.text(
      f"SC-{'N/A' if str_co2_scd30 is None else str_co2_scd30} {unit_co2}", 0, 55)
    
  # oled.text(
  #     f"DT-{'N/A' if str_temp_ds18 is None else str_temp_ds18} {unit_temp}", 0, 60)

  oled.show()


# def connectingToInternetScreen():
#   oled.fill(0)
#   oled.text('Connecting to', 0, 20)
#   oled.text('Internet...', 3, 30)
#   oled.show()


# Connecting to internet:
# if is_available_ssd1306:
#   connectingToInternetScreen()
net_connect.connect()
gc.collect()
# Screen Test
# updateScreen()


# Initial Sensor values:
str_temp_ds18 = None
str_temp_bme280 = None
str_humi_bme280 = None
str_pres_bme280 = None
str_temp_scd30 = None
str_humi_scd30 = None
str_co2_scd30 = None

# Update frequency (Seconds):
update_freq = 5


while True:
  # Reading DS18B20 Sensor
  if is_available_ds18:
    ds_sensor.convert_temp()
    for rom in roms:
      try:
        temp_ds18 = ds_sensor.read_temp(rom)
        str_temp_ds18 = f"{temp_ds18:.2f}"
        print(f"DS18B reading for rom: {rom}: Temperature:{str_temp_ds18}")
      except BaseException as e:
        print("Could not found any DS18B sensor on assigned pin.")

  # Reading BME280 Sensor
  if is_available_bme280:
    str_t_p_h_bme280 = bme.values
    str_temp_bme280 = str_t_p_h_bme280[0]
    str_pres_bme280 = str_t_p_h_bme280[1]
    str_humi_bme280 = str_t_p_h_bme280[2]
    print(
      f"BME280 readings: Temperature:{str_temp_bme280} Pressure:{str_pres_bme280} Humidity:{str_humi_bme280}")

  # Reading SCD30 Sensor
  if is_available_scd30:
    # Wait for sensor data to be ready to read (by default every 2 seconds)
    if scd30.get_status_ready() == 1:
      str_c_t_h_scd30 = list(map(str, scd30.read_measurement()))
      str_co2_scd30 = str_c_t_h_scd30[0]
      str_temp_scd30 = str_c_t_h_scd30[1]
      str_humi_scd30 = str_c_t_h_scd30[2]
      print(
        f"SCD30 readings: Temperature:{str_temp_scd30} CO2 ppm:{str_co2_scd30} Humidity:{str_humi_scd30}")
    else:
      print("SCD30 readings: Waiting for next cycle for the result.")

  # Updating OLED Screen
  if is_available_ssd1306:
    updateScreen(
      str_humi_bme280=str_humi_bme280,
      str_temp_bme280=str_temp_bme280,
      str_pres_bme280=str_pres_bme280,
      str_temp_ds18=str_temp_ds18,
      str_humi_scd30=str_humi_scd30,
      str_temp_scd30=str_temp_scd30,
      str_co2_scd30=str_co2_scd30,
    )

  print('-----------------------------------------------------------')
  # Takes atleast 1ms to clean garbage objects created,
  # prevents heap overflow crashes in limited RAM space.
  gc.collect()
  # Sleep for required duration before reading next value.
  sleep(update_freq)
