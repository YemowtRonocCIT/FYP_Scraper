import psycopg2
import traceback

CONNECTION = "dbname=%s user=%s host=%s password=%s"

class DatabaseInterface(object):

    def __init__(self, db_name, db_user, db_password, host):
        """
        Initializes the DatabaseInterface class. The class requires a database 
        name, user and password to connect to the database. The host allows for
        extensibility and allow remote connections to servers. The class was 
        written to interact with PostgreSQL using psycopg2.

        db_name (str): Name of the database to interact with
        db_user (str): Username credential to access the database
        db_password (str): Password credential to access the database
        host (str): Host location of the database. Should be an IP address, or
            localhost
        """
        try:
            self._conn = psycopg2.connect(CONNECTION % (db_name, db_user, host, 
                                                                db_password))
            self._conn.autocommit = True
        except:
            traceback.print_exc()

        self._cursor = self._conn.cursor()

    def select(self, sql, data=None):
        """
        Returns all rows from a standard SELECT query.

        sql (str): Parameterized sql SELECT query
        data (tuple): Data to be inserted into sql string
        """
        self._cursor.execute(sql, data)
        rows = self._cursor.fetchall()
        return rows

    def execute(self, sql, data):
        """
        Executes a standard statement (INSERT, UPDATE, etc.) with
        data being inserted into the string to prevent SQL Injection attacks.

        sql (str): Parameterized SQL statement
        data (tuple): Data to be inserted into the sql string
        """
        try:
            self._cursor.execute(sql, data)
        except psycopg2.IntegrityError:
            # Should run in case of repeated UNIQUE table values
            traceback.print_exc()
            self._conn.rollback()
        except:
            traceback.print_exc()
            self._conn.rollback()
