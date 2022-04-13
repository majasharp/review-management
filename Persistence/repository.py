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

    def execute_query(self, query, val = None):
        self.cursor.execute(query, val)
        return self.cursor.fetchall() 


    def execute_command(self, query, val): #For inserting values into DB
        self.cursor.execute(query, val)
        self.rmsdb.commit()


    def returnSingleRow (self, query, val):
        self.cursor.execute(query, val)
        result = self.cursor.fetchone() #saves tuple to result
        return result[0] #returns the first result in the tuple
        #return self.cursor.fetchone() #returns value as a tuple, not ideal

    def get_rows(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def update_status_column(self, query, params):
        self.cursor.execute(query, params)
        self.rmsdb.commit()







