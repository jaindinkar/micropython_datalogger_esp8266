# Intermediatory class for handling the SD card storage.
import os
from libs.sdcard import SDCard
# import micropython

class Storage:
    def __init__(self, spi, spi_en, mnt_pt="/sdmc", f_path="/log.txt"):
        if spi is None:
            raise ValueError("An SPI object is required.")
        if spi_en is None:
            raise ValueError("A Pin object is required for SPI_en.")
        
        self.spi = spi
        self.spi_en = spi_en
        self.mnt_pt = mnt_pt
        self.f_path = f_path
        self.init_storage()

    def init_storage(self):
        self.unmount_storage()
        try:
            self.sd = SDCard(self.spi, self.spi_en)
            self.vfs = os.VfsFat(self.sd)
        except BaseException as e:
            print(f"[SD INIT ERROR] SD card: Path:{self.mnt_pt} Error: {e}")
        
        # os.mount(self.vfs, self.mnt_pt)
        # os.mount(slef.sd, self.mnt_pt)
        # print(micropython.mem_info(1))

    def mount_storage(self):
        try:
            os.mount(self.vfs, self.mnt_pt)
        except BaseException as e:
            print(f"[MOUNT ERROR] SD card: Path:{self.mnt_pt} Error: {e}")

    def unmount_storage(self):
        try:
            os.umount(self.mnt_pt)
        except BaseException as e:
            print(f"[UNMOUNT ERROR] SD card: Path:{self.mnt_pt} Error: {e}")

    def storage_content(self):
        self.mount_storage()
        try:
            dir_list = os.listdir(self.mnt_pt)
        except BaseException as e:
            return(f"[LIST ERROR] SD Card: Error retreiving directory List! Error: {e}")
        else:
            return(dir_list)
        finally:
            self.unmount_storage()

    def write_data(self, *data_pts):
        # Comma separated values in log.
        # Order is determined by pos of arguments.
        self.mount_storage()
        try:
            with open(f"{self.mnt_pt}{self.f_path}", "a") as f:
                f.write(f"{','.join(data_pts)}\n")
                f.flush()
        except OSError:
            print(f"Log file not found! Creating a new {self.f_path[1:]} file.")
            with open(f'{self.mnt_pt}{self.f_path}', "x+") as f:
                f.write(f"{','.join(data_pts)}\n")
                f.flush()
        finally:
            self.unmount_storage()
