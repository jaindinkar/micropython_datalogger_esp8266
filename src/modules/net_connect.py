import network
from config.wifi import wifi_ssid, wifi_pass

def connect():
  try:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('Connecting to internet...')
    wlan.connect(wifi_ssid, wifi_pass)
    while wlan.isconnected() == False:
      pass
    print('Connection successful')
    print(wlan.ifconfig())
    return True
  except OSError as e:
    print('An error occured while connecting to internet!!')
    return False
