import json

class DataBaseConfig:

    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user  = user
        self.password = password
        self.db = db    

    def get_host(self):
        return self.host

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password
    
    def get_db(self):
        return self.db

    def get_port(self):
        return self.port

class DataBaseConfigReader:

    def read_db_config(self, filePath):
        file = open(filePath)
        data = json.load(file)

        return DataBaseConfig(data['host'], data['port'], data['user'], data['password'], data['db'])