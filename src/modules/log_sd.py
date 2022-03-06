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
        if not self.__init_storage():
            raise Exception("Storage Initialization Failed.")

    def __init_storage(self):
        if not self.__unmount_storage():
            print(f"No previous mount point found for SD card: Path:{self.mnt_pt}")
        try:
            self.sd = SDCard(self.spi, self.spi_en)
            self.vfs = os.VfsFat(self.sd)
        except BaseException as e:
            print(f"[SD INIT ERROR] SD card: Path:{self.mnt_pt} Error: {e}")
            return(False)
        else:
            return(True)
        
        # os.mount(self.vfs, self.mnt_pt)
        # os.mount(slef.sd, self.mnt_pt)
        # print(micropython.mem_info(1))

    def __mount_storage(self):
        try:
            os.mount(self.vfs, self.mnt_pt)
        except BaseException as e:
            print(f"[SD MOUNT ERROR] SD card: Path:{self.mnt_pt} Error: {e}")
            return(False)
        else:
            return(True)

    def __unmount_storage(self):
        try:
            os.umount(self.mnt_pt)
        except BaseException as e:
            print(f"[SD UNMOUNT ERROR] SD card: Path:{self.mnt_pt} Error: {e}")
            return(False)
        else:
            return(True)

    def print_storage_content(self):
        if self.__mount_storage():
            try:
                # os.listdir is memory hungry!
                # files = os.listdir(self.mnt_pt)
                files_iterator = os.ilistdir(self.mnt_pt)
            except BaseException as e:
                print(f"[SD LIST ERROR] SD Card: Error retreiving directory List! Error: {e}")
            else:
                print("File List Below ===> []. Empty dir won't print anything.")
                for file in files_iterator:
                    print(file)
            finally:
                self.__unmount_storage()
        else:
            raise Exception("Can't mount the storage block.")

    def write_data(self, *data_pts):
        # Comma separated values in log.
        # Order is determined by pos of arguments.
        if self.__mount_storage():
            try:
                with open(f"{self.mnt_pt}{self.f_path}", "a") as f:
                    f.write(f"{','.join(data_pts)}\n")
                    f.flush()
            except BaseException as e:
                print(f"[SD FILE APPEND ERROR] Assuming file not found, creating a new {self.f_path[1:]} file. Error: {e}")
                try:
                    with open(f'{self.mnt_pt}{self.f_path}', "x+") as f:
                        f.write(f"{','.join(data_pts)}\n")
                        f.flush()
                except BaseException as e:
                    print(f"[SD FILE WRITE ERROR] SD Card: File creation and write Failed. Error: {e}")
                    raise Exception(f"{e}")
            finally:
                self.__unmount_storage()
        else:
            raise Exception("Can't mount the storage block.")
