## ESP32 SD Card Tests

### Description
- Implementation for Sd Card in ESP32 using VSPI.
- No modification in the original driver is needed to work with esp32 as of 17/02/2022. (Link to driver)[https://github.com/micropython/micropython/blob/master/drivers/sdcard/sdcard.py]

#### General Hardware Connection Points
- Maintain short and proper connections to the device, this module is succeptable to the undervoltage and underpower.
- Test your du-point connectors before use (they should be conductive with resistance lesser than 1 ohm).
- Use a 5 volt supply for the operation. Less than that might cause problems though 4.75 v also works fine in our case.
