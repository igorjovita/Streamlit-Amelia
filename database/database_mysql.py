import mysql.connector
import os

class DataBaseMysql:

    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def connect(self):
        mydb = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            passwd=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            autocommit=True)
        self.connection = mydb
        self.cursor = self.connection.cursor(buffered=True)
        return self.cursor
        
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None





