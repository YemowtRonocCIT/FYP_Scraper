import traceback

DATA_KEY = 'data'
TIME_KEY = 'time'
ID_KEY = 'id'

class SigfoxParser(object):

    def __init__(self):
        pass

    def retrieve_device_type_ids_from_response(self, device_types_response):
        """
        This function will retrieve a list of Sigfox Device Type IDs from a 
        response to a Device Types request. The returned value is a list of str
        values.

        device_types_response (requests.models.Response): Standard response
        from the requests module. Should be request for device types. 
        """
        device_types = device_types_response[DATA_KEY]

        device_type_ids = []
        for device_type in device_types:
            current_id = device_type[ID_KEY]
            device_type_ids.append(current_id)

        return device_type_ids

    def retrieve_device_id_from_response(self, device_ids_response):
        """
        This function will retrieve a list of Sigfox Device IDs from a response
        to a Devices request. The returned value is a list of str values.

        device_ids_response (requests.models.Response): Standard response from
        the requests module. Should be request for devices.
        """
        devices = []

        device_ids = device_ids_response[DATA_KEY]
        for device in device_ids:
            devices.append(device[ID_KEY])

        return devices

    def retrieve_device_messages_from_response(self, device_messages_response):
        """
        Retrieves the messages from a Sigfox Device Messages response. The 
        returned value is a list of str values. 

        device_messages_response (requests.models.Response): Standard response
        from the requests module. Should be request for device messages.
        """
        messages = device_messages_response[DATA_KEY]
        list_of_messages = []

        for message in messages:
            message_tuple = (message[DATA_KEY], message[TIME_KEY])
            list_of_messages.append(message_tuple)
        
        return list_of_messages

    def convert_message_from_hex(self, hex_encoded_message):
        """
        Decodes a hexadecimal encoded message, decoded to standard str.

        hex_encoded_message (str): Hex encoded string to be decoded.
        If the message if not valid Hexadecimal, it is returned as is.
        """
        try:
            decoded = bytearray.fromhex(hex_encoded_message).decode()
            return decoded
        except ValueError:
            traceback.print_exc()
            print("Supposed Message: %s" % (hex_encoded_message))
            return hex_encoded_message
