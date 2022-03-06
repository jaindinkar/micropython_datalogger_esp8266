# Intermediatory class for handling the SSD1306 OLED display.
from ssd1306 import SSD1306_I2C

class OLED:
    def __init__(self, oled_width, oled_height, i2c):
        if i2c is None:
            raise ValueError("An I2C object is required.")
        if oled_width is None:
            raise ValueError("OLED width is required.")
        if oled_height is None:
            raise ValueError("OLED height is required.")
        
        self.i2c = i2c
        self.width = oled_width
        self.height = oled_height
        if not self.__init_display():
            raise Exception("OLED Initialization Failed.")

    def __init_display(self):
        try:
            self.oled = SSD1306_I2C(self.width, self.height, self.i2c)
        except BaseException as e:
            print(f"[OLED INIT ERROR]: {e}")
            return(False)
        else:
            return(True)
    
    def updateScreen(self, **kwargs):
        # Unit constants
        unit_humi = '%RH'
        unit_temp = 'degC'
        unit_pres = 'mBar'
        unit_co2 = 'ppm'

        self.oled.fill(0)
        self.oled.text(
            f"BH-{'N/A' if kwargs['str_humi_bme280'] is '' else kwargs['str_humi_bme280']} {unit_humi}", 0, 0)
        self.oled.text(
            f"BT-{'N/A' if kwargs['str_temp_bme280'] is '' else kwargs['str_temp_bme280']} {unit_temp}", 0, 10)
        self.oled.text(
            f"BP-{'N/A' if kwargs['str_pres_bme280'] is '' else kwargs['str_pres_bme280']} {unit_pres}", 0, 20)

        self.oled.text(
            f"SH-{'N/A' if kwargs['str_humi_scd30'] is '' else kwargs['str_humi_scd30']} {unit_humi}", 0, 35)
        self.oled.text(
            f"ST-{'N/A' if kwargs['str_temp_scd30'] is '' else kwargs['str_temp_scd30']} {unit_temp}", 0, 45)
        self.oled.text(
            f"SC-{'N/A' if kwargs['str_co2_scd30'] is '' else kwargs['str_co2_scd30']} {unit_co2}", 0, 55)
        
        self.oled.show() 

    def connectingToInternetScreen(self):
        self.oled.fill(0)
        self.oled.text('Connecting to', 0, 20)
        self.oled.text('Internet...', 3, 30)
        self.oled.show()
