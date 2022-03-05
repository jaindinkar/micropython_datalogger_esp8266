import urequests
from config.zapier import zap_webhook_url

def sendData(temp_bme, humi_bme, pres_bme, temp_ds18):

  # Release the webhook to log data to google sheets:
  try:
    payload = {
      "temp_bme280": temp_bme,
      "humi_bme280": humi_bme,
      "pres_bme280": pres_bme,
      "temp_ds18b": temp_ds18
    }

    request_headers = {'Content-Type': 'application/json'}

    request = urequests.post(
      zap_webhook_url,
      json=payload,
      headers=request_headers
    )
    print(f"Post Response status: {request.status_code} {request.reason}")
    request.close()

  except BaseException as e:
    print('Failed to log sensor readings online.')
