import logging

class MessageParser(object):

    def retrieve_button_pressed(self, char):
        """
        This function retrieves information about whether or not the button
        is pressed based on the documented encoding of the messages. Returns
        -1 if the message is not valid. Otherwise, bool is returned.

        message (str): Character from message
        """
        BUTTON_PRESSED = 'B'
        BUTTON_NOT_PRESSED = 'N'

        value = False

        if char == BUTTON_PRESSED:
            value = True
        elif char == BUTTON_NOT_PRESSED:
            value = False
        else:
            value = -1
        
        return value

    def check_temp_sensed(self, char):
        """
        Returns value based on whether or not the temperature was sensed. 

        message (str): Character from message
        """
        TEMPERATURE_NOT_DETECTED = 'Z'

        value = False

        if char != TEMPERATURE_NOT_DETECTED:
            value = True

        return value

    def check_vibration_sensed(self, char):
        """
        Returns value based on whether or not the vibration was sensed.

        char (str): Character from message
        """
        VIBRATION_NOT_SENSED = 'Z'

        value = False

        if char != VIBRATION_NOT_SENSED:
            value = True

        return value

    def convert_temperature(self, char):
        """
        Returns int value referring to the highest temperature that could 
        be detected at that encoding

        char (str): Character from message
        """
        ZERO_CHAR = 'A'
        ONE_CHAR = 'B'
        TWO_CHAR = 'C'
        THREE_CHAR = 'D'
        FOUR_CHAR = 'E'
        FIVE_CHAR = 'F'
        TEN_CHAR = 'G'
        FIFTEEN_CHAR = 'H'
        TWENTY_CHAR = 'I'
        TWENTY_FIVE_CHAR = 'J'
        THIRTY_CHAR = 'K'
        THIRTY_FIVE_CHAR = 'L'
        FORTY_CHAR = 'M'
        GREATER_FORTY_CHAR = 'N'

        map_values = {
            ZERO_CHAR: 0,
            ONE_CHAR: 1,
            TWO_CHAR: 2,
            THREE_CHAR: 3,
            FOUR_CHAR: 4,
            FIVE_CHAR: 5,
            TEN_CHAR: 10,
            FIFTEEN_CHAR: 15,
            TWENTY_CHAR: 20,
            TWENTY_FIVE_CHAR: 25,
            THIRTY_CHAR: 30,
            THIRTY_FIVE_CHAR: 35,
            FORTY_CHAR: 40,
            GREATER_FORTY_CHAR: 50
        }

        value = -127

        if char.upper() in map_values:
            value = map_values[char]
    
        if char.islower():
            value = value * -1
        
        return value

    def convert_vibration(self, char):
        """
        Returns float value based on the char given.

        char (str): Character from message
        """
        ZERO_READING = 'Z'
        TEN_READING = 'B'
        TWENTY_READING = 'C'
        THIRTY_READING = 'D'
        FORTY_READING = 'E'
        FIFTY_READING = 'F'
        SIXTY_READING = 'G'
        SEVENTY_READING = 'H'
        EIGHTY_READING = 'I'
        NINETY_READING = 'J'
        HUNDRED_READING = 'K'
        OFF_SCALE_READING = 'L'

        map_values = {
            ZERO_READING: 0.00,
            TEN_READING: 0.10,
            TWENTY_READING: 0.20,
            THIRTY_READING: 0.30,
            FORTY_READING: 0.40,
            FIFTY_READING: 0.50,
            SIXTY_READING: 0.60,
            SEVENTY_READING: 0.70,
            EIGHTY_READING: 0.80,
            NINETY_READING: 0.90,
            HUNDRED_READING: 1.00,
            OFF_SCALE_READING: 2.00
        }

        value = 0.000

        if char in map_values:
            value = map_values[char]
        
        return value

    def calculate_temperature_value(self, char, temperature_sensed):
        """
        Calculates the value to be added to the database for the temperature.

        char (str): Single character encoded by the Arduino
        """
        temperature = None
        if temperature_sensed == True:
            temperature = self.convert_temperature(char)

        if temperature == None:
            temperature = -127
        
        return temperature

    def calculate_vibration_value(self, char, vibration_sensed):
        """
        Calculates the value to be added to the database for the vibration.

        char (str): Single character encoded by the Arduino
        """
        vibration_value = None      
        if vibration_sensed == True:
            vibration_value = self.convert_vibration(char)

        if vibration_value == None:
            vibration_value = 0.00

        return vibration_value


    def insert_message_to_latest_message(self, message, db, node_id):
        """
        Inserts relevant data for a message into the database, with given
        connection to the node_id. 

        message (str): Decoded message as sent to Sigfox
        db (scraper.PostgresInteraction): PostgresInteraction class to allow 
        communication with database
        node_id (str): ID of node as given by the database
        """
        BUTTON_CHAR_INDEX = 0
        TEMPERATURE_CHAR_INDEX = 1
        VIBRATION_CHAR_INDEX = 2
        APPROPRIATE_MESSAGE_LENGTH = 3

        if len(message) == APPROPRIATE_MESSAGE_LENGTH:

            button_char = message[BUTTON_CHAR_INDEX]
            temperature_char = message[TEMPERATURE_CHAR_INDEX]
            vibration_char = message[VIBRATION_CHAR_INDEX]
            
            button_pressed = self.retrieve_button_pressed(button_char)
            if button_pressed != -1:

                temperature_sensed = self.check_temp_sensed(temperature_char)
                temperature_number = self.calculate_temperature_value(
                                            temperature_char, temperature_sensed)  

                vibration_sensed = self.check_vibration_sensed(vibration_char)
                vibration_value = self.calculate_vibration_value(
                                            vibration_char, vibration_sensed)
                
                db.add_latest_message(node_id, button_pressed, temperature_sensed, 
                    vibration_sensed, temperature_number, vibration_value)

        else:
            logging.debug("Invalid message: %s" % (message))
