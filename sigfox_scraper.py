"""
This module features the SigfoxScraper() class. The class hides the 
implementation details for requests to the sigfox network. It returns
key data, including device type IDs, devices, and device messages.
"""

import requests
import json

DEVICE_TYPES_URL = "https://backend.sigfox.com/api/devicetypes/"
DEVICE_INFO_URL = "https://backend.sigfox.com/api/devices/%s/"
DEVICE_MESSAGES_URL = "https://backend.sigfox.com/api/devices/%s/messages"

DATA_KEY = 'data'
ID_KEY = 'id'


class SigfoxScraper(object):

    def __init__(self, username=None, password=None):
        """
        Initializes an instance of SigfoxScraper. If login details are given,
        they will be stored for use in the requests later. 

        username: str
        password: str
        """
        if username:
            self._login = username
        else:
            self._login = None

        if password:
            self._password = password
        else:
            self._password = None

    def request_list_of_device_type_ids(self): 
        """
        Returns in dict format, the device type IDs from the sigfox network
        for the registered user. 
        """
        url = DEVICE_TYPES_URL
        response = requests.get(url, auth=(self._login, self._password))
        device_type_ids = response.text
        device_type_ids = json.loads(device_type_ids)

        return device_type_ids

    def request_devices(self):
        pass

    def request_device_messages(self, device_id):
        """
        Returns in dict format, the response from the sigfox network when 
        requesting messages for a given device ID.

        device_id: str
        """
        url = DEVICE_MESSAGES_URL % (device_id)
        response = requests.get(url, auth=(self._login, self._password))
        messages = response.text
        messages = json.loads(messages)
        return messages
    
    def store_authorisation_details(self, username, password):
        """
        Stores login details of the user in the class. 

        username: str
        password: str
        """
        self._login = username
        self._password = password
        pass

    def print_response(self, response):
        """
        Prints reponse details from requests module, for a given response.

        response: requests.models.Response
        """
        print("Status Code: %d" % (response.status_code))
        print("Response Content Type: %s" % (response.headers['content-type']))
        print("Character Encoding: %s" % (response.encoding))
        print("Text of response: \n\n%s\n\n" % (response.text))
        print("JSON response: %s" % (response.json()))