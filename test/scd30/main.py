import time
from machine import I2C, Pin
from libs.scd30_sm import SCD30

i2c = I2C(scl=Pin(5), sda=Pin(4))
scd30 = SCD30(i2c, 0x61)

while True:
  # Wait for sensor data to be ready to read (by default every 2 seconds)
  if scd30.get_status_ready() == 1:
    print(scd30.read_measurement())
  else:
    print("Waiting 3 more seconds for the result.")

  time.sleep(3)
