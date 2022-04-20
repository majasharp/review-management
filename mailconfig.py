import json

class MailConfig:
    def __init__(self, senderEmail, senderPassword, smtpServer, smtpPort, extraRecipients):
        self.senderEmail = senderEmail
        self.senderPassword = senderPassword
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.extraRecipients = extraRecipients

    def get_sender_email(self):
        return self.senderEmail

    def get_sender_password(self):
        return self.senderPassword

    def get_smtp_server(self):
        return self.smtpServer

    def get_smtp_port(self):
        return self.smtpPort

    def get_extra_recipients(self):
        return self.extraRecipients

class MailConfigReader:
    def deserialize(self, filePath):
        file = open(filePath)
        data = json.load(file)

        return MailConfig(data['senderEmail'], data['senderPassword'], data['smtpServer'], data['smtpPort'], data['extraRecipients'])