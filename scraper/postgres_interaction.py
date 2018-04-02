from scraper.postgres_interface import PostgresInterface

class PostgresInteraction(PostgresInterface):

    def __init__(self, db_name, db_user, db_password, host):
        """
        Constructor for PostgresInteraction class. It requires the details to
        connect to the database, and will use the PostgresInterface() class
        to simplify interactions.

        db_name (str): The name of the database that will be used
        db_user (str): The username to connect to the database, to allow the 
        correct permissions to each user of the database.
        db_password (str): The password to authenticate the users access to the
        database.
        host (str): IP address of database system, to allow remote connections
        """
        super().__init__(db_name, db_user, db_password, host)

    def add_node(self, sigfox_id, is_active):
        """
        Inserts a node into the database, with the given sigfox ID and status.

        sigfox_id (str): Given Sigfox ID, to identify the node
        is_active (bool): True if the node is currently being listened for,
        False if the node is disabled.
        """
        sql = """INSERT INTO node (node_id, sigfox_id, active)
        VALUES (default, %s, %s)
        ON CONFLICT (sigfox_id) DO UPDATE
        SET active = %s"""
        data = (sigfox_id, is_active, is_active)
        if self.execute(sql, data):
            return True
        else:
            return False

    def set_node_status(self, status, sigfox_id):
        """
        Change the status of the node with the given Sigfox ID.

        status (bool): Status of the node.
        sigfox_id (str): Given sigfox ID for node.
        """
        sql = """UPDATE node
        SET active = %s
        WHERE sigfox_id = %s"""
        data = (status, sigfox_id)
        if self.execute(sql, data):
            return True
        else:
            return False

    def remove_node(self, sigfox_id):
        """
        Removes the node from the database with the given Sigfox ID.

        sigfox_id (str): Given Sigfox ID for the node
        """
        sql = """DELETE FROM node
        WHERE sigfox_id = %s;"""
        data = (sigfox_id, )
        if self.execute(sql, data):
            return True
        else:
            return False

    def retrieve_all_nodes(self):
        """
        Gets all nodes from the database.
        """
        sql =  """SELECT node_id, sigfox_id, active
        FROM node"""
        rows = self.select(sql)
        return rows

    def retrieve_node_by_sigfox_id(self, sigfox_id):
        """
        Retrieves specific node from database with given Sigfox ID.

        sigfox_id (str): Given sigfox ID
        """
        sql = """SELECT node_id, sigfox_id, active
        FROM node
        WHERE sigfox_id = %s"""
        data = (sigfox_id, )
        rows = self.select(sql, data)
        return rows

    def add_latest_message(self, node_id, button_pressed, temperature_sensed, 
                                vibration_sensed, temperature, vibration):
        """
        Adds message details to database. The details of each sensor are 
        decoded before being inserted into the database.

        node_id (int): ID of node as given by the database
        button_pressed (bool): True if the button is currently being pressed
        temperature (character): Encoded character value to be converted
        vibration (character): Encoded character value to be converted
        """
        sql = """INSERT INTO last_message(node_id, button_press, 
            temp_sensed, vib_sensed, temperature, vibration, 
            time_entered) 
        VALUES (%s, %s, %s, %s, %s, %s, current_timestamp)
        ON CONFLICT (node_id) DO UPDATE
        SET button_press = %s,
            temp_sensed = %s,
            vib_sensed = %s,
            temperature = %s,
            vibration = %s,
            time_entered = current_timestamp;"""
        data = (node_id, button_pressed, temperature_sensed, vibration_sensed,
                        temperature, vibration, button_pressed, temperature_sensed,
                        vibration_sensed, temperature, vibration)
        if self.execute(sql, data):
            return True
        else:
            return False