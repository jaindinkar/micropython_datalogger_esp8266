# Intermediatory class for handling the SD card storage.
class storage:
    def __init__(self, spi, spi_en):
        self.spi = spi
        self.spi_en = spi_en
