import mysql.connector

class Repository:

    def __init__(self, dataBaseConfig):
        self.rmsdb = mysql.connector.connect(
            host = dataBaseConfig.get_host(),
            port = dataBaseConfig.get_port(),
            user = dataBaseConfig.get_user(),
            password = dataBaseConfig.get_password(),
            database = dataBaseConfig.get_db()
        )

        self.cursor = self.rmsdb.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall() 
        # do not touch

    def insert_values(self, query, val): #For inserting values into DB
        self.cursor.execute(query, val)
