import os
from machine import Pin, SPI
from sdcard import SDCard

hspi_en = Pin(15) # D3 Flash button might not work. Can be any gpio pin. Follow boot pin caution if reset occurs.
hspi = SPI(1, baudrate=80000000, polarity=0, phase=0) # SPI will take GPIO 12,13,14 | D6,D7,D5 automatically.

sd = SDCard(hspi, hspi_en)
vfs = os.VfsFat(sd)
os.mount(vfs, '/sdmc')
# os.mount(sd, '/sdmc')

print('Root directory:{}'.format(os.listdir()))
print('SD Card contains:{}'.format(os.listdir("/sdmc")))

os.umount("/sdmc")

# Changing SD Card:
# os.umount("/sdmc")
# sd = SDCard(hspi, hspi_en) 
# vfs = os.VfsFat(sd)
# os.mount(vfs, '/sdmc')

# SD Card presence detection:
# sd = SDCard(hspi, hspi_en) # This also throws the correct error when sd card is not present. No Sd card.
# vfs = os.VfsFat(sd) # this can be used to check if sd card is there or not.
# File write would throw: Error EONT

# OS command instructions can be found from:
# https://docs.micropython.org/en/latest/library/os.html

# 1. To read file from the root directory:
# f = open('sample.txt', 'r')
# print(f.read())
# f.close()

# 2. To create a new file for writing:
# f = open('sample2.txt', 'w')
# f.write('Some text for sample 2')
# f.close()

# 3. To append some text in existing file:
# f = open('sample3.txt', 'a')
# f.write('Some text for sample 3')
# f.close()

# 4. To delete a file:
# os.remove('file to delete')

# 5. To list all directories and files:
# os.listdir()

# 6. To create a new folder:
# os.mkdir('sample folder')

# 7. To change directory:
# os.chdir('directory you want to open')

# 8. To delete a folder:
# os.rmdir('folder to delete')

# 9.  To rename a file or a folder:
# os.rename('current name', 'desired name')
