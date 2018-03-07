import requests
import json

DEVICE_TYPES_URL = "https://backend.sigfox.com/api/devicetypes/"
DEVICE_INFO_URL = "https://backend.sigfox.com/api/devices/%s/"
DEVICE_MESSAGES_URL = "https://backend.sigfox.com/api/devices/%s/messages"

DATA_KEY = 'data'
ID_KEY = 'id'


class SigfoxScraper(object):

    def __init__(self, username=None, password=None):
        if username:
            self._login = username
        else:
            self._login = None

        if password:
            self._password = password
        else:
            self._password = None

    def request_list_of_devices(self):
        url = DEVICE_TYPES_URL
        response = requests.get(url, auth=(self._login, self._password))
        device_types = response.text
        device_types = json.loads(device_types)
        device_types = device_types[DATA_KEY]
        device_type_ids = []
        for device in device_types:
            device_type_ids.append(device[ID_KEY])

        return device_type_ids

    def request_device_messages(self, device_id):
        url = DEVICE_MESSAGES_URL % (device_id)
        response = requests.get(url, auth=(self._login, self._password))
        self.print_response(response)
        messages = response.text
        messages = json.loads(messages)
        messages = messages[DATA_KEY]
        return messages
    
    def submit_authorisation_details(self, username, password):
        self._login = username
        self._password = password
        pass

    def print_response(self, response):
        print("Status Code: %d" % (response.status_code))
        print("Response Content Type: %s" % (response.headers['content-type']))
        print("Character Encoding: %s" % (response.encoding))
        print("Text of response: \n\n%s\n\n" % (response.text))
        print("JSON response: %s" % (response.json()))