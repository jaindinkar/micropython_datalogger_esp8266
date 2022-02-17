from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)

while True:
  led.value(True)
  sleep(1)
  led.value(False)
  sleep(1)
