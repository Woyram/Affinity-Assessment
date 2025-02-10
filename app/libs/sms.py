import json

import requests

from app import config, language
from app.libs.logger import Logger

class SMS():

    def __init__(self):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.logger = Logger()

    def sendSMS(self, sender, msg):
        print("Sending SMS")

        try:
            print("Sending SMS to the client")

            # Validate Number
            validatedNumber = self.validateNumber(sender)

            headers = {
                "Authorization": config.SMS_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            payload = json.dumps({
                "messages": [
                    {
                        "destinations": [
                            {
                                "to": validatedNumber
                            }
                        ],
                        "from": "WOYRAM",
                        "text": msg
                    }
                ]
            })

            print("-----------------------------------------------------------------------------------")
            print(payload)
            print("-----------------------------------------------------------------------------------")

            sendSMS = requests.post(config.BASIC_SMS_BASE_URL, data=payload, headers=headers, verify=True)

            print("SMS Response is: {}".format(sendSMS))
            print(json.loads(sendSMS.content))
            response = json.loads(sendSMS.content)

            if sendSMS.status_code == 200:
                return response
            else:
                return response

        except Exception as e:
            print("The Exception is: {}".format(e))
            return True

    def sendHubtelSMS(self, recipient, message):
        print("Sending Hubtel SMS")

        try:
            print("Trying")
            payload = {}
            headers = {}
            url = "{}?clientid={}&clientsecret={}&from={}&to={}&content={}".format(config.HUBTEL_URL, config.HUBTEL_CLIENT_ID, config.HUBTEL_CLIENT_SECRETE, config.HUBTEL_FROM, recipient, message)

            response = requests.request("GET", url, headers=headers, data=payload)
            print("o;o;o;o;o;o;o;o;o;o")
            print(response)
            print(response.text)
            print(json.loads(response.content))
            return True

        except Exception as e:
            print("The Exception is: {}".format(e))
            return False

    def sendMNOTIFYSMS(self, recipient, message):
        print("Sending Message Via MNOTIFY")

        try:
            print("Trying")
            payload = {}
            headers = {}
            url = "{}?key={}&to={}&msg={}&sender_id={}".format(config.MNOTIFY_URL, config.MNOTIFY_KEY, recipient, message, config.MNOTIFY_SENDER_ID)

            response = requests.request("GET", url, headers=headers, data=payload)
            print("o;o;o;o;o;o;o;o;o;o")
            print(response)
            print(response.text)
            print(json.loads(response.content))
            return True

        except Exception as e:
            print("The Exception is: {}".format(e))
            return False

    def sendPillowSMS(self, recipient, message):
        print("Sending Message Via Pillow Soft")

        try:
            print("Trying")
            headers = {}
            url = config.PILLOW_SOFT_URL.format(config.PILLOW_SOFT_API_KEY)

            payload = {'sender': 'IEREIP_ENT',
                       'message': message,
                       'receipients': recipient}
            files = []

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            print("o;o;o;o;o;o;o;o;o;o")
            print(response)
            print(response.text)
            print(json.loads(response.content))
            return True

        except Exception as e:
            print("The Exception is: {}".format(e))
            return False

    def sendBulkSMS(self, listSenders, message):
        print("Sending Bulk SMS")

        return False

    def validateNumber(self, number):
        print("Validate Number: {}".format(number))

        if (len(number) < 12) and (len(number) == 10):
            print("Format number to match InfoBip")

            senderNumber = "233"+number[-9:]
            print("-----------------------------------------------------------------------------------")
            print("Validated number is: {}".format(senderNumber))
            return senderNumber
        else:
            return number
