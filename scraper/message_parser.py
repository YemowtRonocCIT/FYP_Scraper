
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
        TEMPERATURE_NOT_DETECTED = 'N'

        value = False

        if char != TEMPERATURE_NOT_DETECTED:
            value = True

        return value

    def check_vibration_sensed(self, char):
        """
        Returns value based on whether or not the vibration was sensed.

        char (str): Character from message
        """
        VIBRATION_NOT_SENSED = 'N'

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
        
        FORTY_DEGREES = 'A'

        value = -127

        if char == FORTY_DEGREES:
            value = 40
    
        if char.islower():
            value = value * -1
        
        return value

    def convert_vibration(self, char):
        """
        Returns float value based on the char given.

        char (str): Character from message
        """

        HIGH_VIBRATION = 'V'

        value = -127.000

        if char == HIGH_VIBRATION:
            value = 0.999
        
        return value

    def insert_message_to_database(self, message, db, node_id):
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

        button_char = message[BUTTON_CHAR_INDEX]
        temperature_char = message[TEMPERATURE_CHAR_INDEX]
        vibration_char = message[VIBRATION_CHAR_INDEX]
        
        button_pressed = self.retrieve_button_pressed(button_char)
        temperature_sensed = self.check_temp_sensed(temperature_char)
        vibration_sensed = self.check_vibration_sensed(vibration_char)

        db.add_sensor_update(node_id, temperature_sensed, vibration_sensed)

        if temperature_sensed:
            temperature_number = self.convert_temperature(temperature_char)
            
        if vibration_sensed:
            vibration_value = self.convert_vibration(vibration_char)

        db.add_message(node_id, button_pressed, temperature_number, vibration_value)
