from scraper.sigfox_scraper import SigfoxScraper
from scraper.postgres_interface import PostgresInterface
from scraper.postgres_interaction import PostgresInteraction
from scraper.sigfox_parser import SigfoxParser
from scraper.message_parser import MessageParser
from login_details import USER, PASSWORD
from login_details import DB_NAME, DB_USER, DB_PASSWORD, HOST

import logging

DATA_KEY = 'data'
ID_KEY = 'id'
NODE_ID_INDEX = 0
LOGGING_FILE = 'scraper.log'

def main():
    """
    Entry point for the scraper. 
    """
    
    # Config the logging output file
    logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG)

    # Start scraping for Sigfox data
    scraper = SigfoxScraper(USER, PASSWORD)
    device_types = scraper.request_device_types()

    # Parse the data to allow conversion and readability
    sigfox_parser = SigfoxParser()
    device_type_ids = sigfox_parser.retrieve_device_type_ids_from_response(device_types)

    # Retrieve device information to pull messages
    devices = {}
    for device_type_id in device_type_ids:
        devices_of_type = scraper.request_devices(device_type_id)
        devices[device_type_id] = sigfox_parser. \
            retrieve_device_id_from_response(devices_of_type)
    
    # Set up database interaction to allow it to be used
    db = PostgresInteraction(DB_NAME, DB_USER, DB_PASSWORD, HOST)    
    message_parser = MessageParser()
    
    for value in devices.values():
        # value can be a list of devices
        for device in value:
            if db.add_node(device, False):
                logging.debug("Node inserted: %s" % device)
            else:
                logging.error("Node could not be inserted: %s" % device)

            payload = None
                
            device_messages = scraper.request_device_messages(device, payload)
            encoded_messages = sigfox_parser.retrieve_device_messages_from_response(device_messages)

            rows = db.retrieve_node_by_sigfox_id(device)
            for row in rows:
                node_id = row[NODE_ID_INDEX]

            MESSAGE_INDEX = 0
            TIME_INDEX = 1
            for encoded_message in encoded_messages:
                message = sigfox_parser.convert_message_from_hex(encoded_message[MESSAGE_INDEX])
                seconds_since_unix_epoch = encoded_message[TIME_INDEX]
                db.add_message(node_id, message, seconds_since_unix_epoch)
                message_parser.insert_message_to_database(message, db, node_id)

if __name__ == '__main__':
    main()