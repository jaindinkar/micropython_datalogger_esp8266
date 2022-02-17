## ESP8266 SD Card Tests

### Description
- Hardware SPI port used on GPIOs 12,13,14,15. Use Pin 15 for SPI_CS with caution as it is used to set device's boot state and might cause resets. (not observed in our case) [Link 1](https://github.com/esp8266/Arduino/issues/2466) [Link 2](https://www.instructables.com/ESP8266-Using-GPIO0-GPIO2-as-inputs/)
- Original driver provided as of 17/02/2022 for ESP8266 sd card access does not properly work in our case. [Link to driver](https://github.com/micropython/micropython/blob/master/drivers/sdcard/sdcard.py) [Adafruit video on this](https://www.youtube.com/watch?v=-1nzG1BdPps) [Link to delay suggestion](https://forum.micropython.org/viewtopic.php?t=3404&start=10#p21454)
- Changes are done in this attached driver to accomodate that.
- Also given expamples in the driver code does not work, we have also provided a sufficient implementation for this in main.py
- Changing the SD Card can be performed by executing a certain set of instructions to update the directory. (see code in main.py)
- If you are getting """OSError: [Errno 1] EPERM""" while accessing the card you might be in a different directory then supposed to be. Use OS filesystem commands to navigate to "/" and unmount the mounted partition.

#### General Hardware Connection Points
- Maintain short and proper connections to the device, this module is succeptable to the undervoltage and underpower.
- Test your du-point connectors before use (they should be conductive with resistance lesser than 1 ohm).
- Use a 5 volt supply for the operation. Less than that might cause problems though 4.75 v also works fine in our case.

### References:
Micropython OS services: [Link](https://docs.micropython.org/en/latest/library/os.html)
