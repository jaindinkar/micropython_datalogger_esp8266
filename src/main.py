from machine import Pin, I2C
from onewire import OneWire
from time import sleep
import urequests

import ds18x20
import ssd1306
import libs.bme280_sm as bme280_sm

import modules.net_connect as net_connect
from config.zapier import zap_webhook_url


# Availablity check:
is_available_ds18 = False
is_available_bme280 = False
is_available_ssd1306 = False

# Unit constants
unit_humi = '%RH'
unit_temp = 'degC'
unit_pres = 'mBar'

# Initial Sensor values:
str_temp_ds18 = None
str_temp_bme280 = None
str_humi_bme280 = None
str_pres_bme280 = None

# Update frequency (Seconds):
update_freq = 30


# ESP8266 I2C Pin assignment
i2c = I2C(scl=Pin(5), sda=Pin(4))
# ESP8266 One Wire Pin assignment
one_wire = OneWire(Pin(13))


# One-wire DS18B20 config:
try:
  ds_sensor = ds18x20.DS18X20(one_wire)
  roms = ds_sensor.scan()
  if len(roms):
    print('Found DS devices: ', roms)
    is_available_ds18 = True
  
except BaseException as e:
  print("Could not found any DS18B sensor on assigned pin.")
  
# I2C OLED Config:
try:
  oled_width = 128
  oled_height = 64
  oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
  is_available_ssd1306 = True
except BaseException as e:
  print('Could not found any SSD1306 OLED on I2C bus.')

# I2C BME280 Config:
try:
  bme = bme280_sm.BME280(i2c=i2c)
  is_available_bme280 = True
except BaseException as e:
  print('Could not found any BME280 Sensor on I2C bus.')
  print(e)

# Function for updating OLED Screen
def updateScreen(
  str_humi_bme280='N/A',
  str_temp_bme280='N/A',
  str_pres_bme280='N/A',
  str_temp_ds18='N/A'
):
  oled.fill(0)
  oled.text('BME280 **>', 0, 0)
  oled.text(f"Humi: {'N/A' if str_humi_bme280 is None else str_humi_bme280} {unit_humi}", 0, 10)
  oled.text(f"Temp: {'N/A' if str_temp_bme280 is None else str_temp_bme280} {unit_temp}", 0, 20)
  oled.text(f"Pres: {'N/A' if str_pres_bme280 is None else str_pres_bme280} {unit_pres}", 0, 30)
  oled.text('', 0, 40)
  oled.text('DS18B **>', 0, 45)
  oled.text(f"Temp: {'N/A' if str_temp_ds18 is None else str_temp_ds18} {unit_temp}", 0, 55)
  oled.show()

def connectingToInternetScreen():
  oled.fill(0)
  oled.text('Connecting to', 0, 20)
  oled.text('Internet...', 3, 30)
  oled.show()

# Connecting to internet:
if is_available_ssd1306:
  connectingToInternetScreen();
net_connect.connect()

# Screen Test
# updateScreen()

while True:
  # Reading DS18B20 Sensor
  if is_available_ds18:
    ds_sensor.convert_temp()
    temp_ds18 = ds_sensor.read_temp(roms[0])
    str_temp_ds18 = f"{temp_ds18:.2f}"
  
  # Reading BME280 Sensor
  if is_available_bme280:
    str_t_p_h_bme280 = bme.values
    str_temp_bme280 = str_t_p_h_bme280[0]
    str_pres_bme280 = str_t_p_h_bme280[1]
    str_humi_bme280 = str_t_p_h_bme280[2]
  
  # Updating OLED Screen
  if is_available_ssd1306:
    updateScreen(
      str_humi_bme280=str_humi_bme280,
      str_temp_bme280=str_temp_bme280,
      str_pres_bme280=str_pres_bme280,
      str_temp_ds18 = str_temp_ds18
    )
  
  # Release the webhook to log data to google sheets:
  try:
    payload = {
      "temp_bme280": str_temp_bme280,
      "humi_bme280": str_humi_bme280,
      "pres_bme280": str_pres_bme280,
      "temp_ds18b": str_temp_ds18
    }
    
    print(payload)
    
    request_headers = {'Content-Type': 'application/json'}

    request = urequests.post(
      zap_webhook_url,
      json=payload,
      headers=request_headers
    )
    print(request.text)
    request.close()

  except BaseException as e:
    print('Failed to log sensor readings online.')
  
  # Sleep for required duration before reading next value.
  sleep(update_freq)
