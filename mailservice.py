import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailService:
    def __init__(self, config):
        self.config = config
    
    def send_mail(self, message, receiver):
        server = smtplib.SMTP_SSL(self.config.get_smtp_server())
        server.connect(self.config.get_smtp_server(), self.config.get_smtp_port())
        server.ehlo()
        server.login(self.config.get_sender_email(), self.config.get_sender_password())

        message = 'Subject: {}\n\n{}'.format('Response to your review from Constella Review Management', message)
        server.sendmail(config.get_sender_email(), receiver, message)
        server.quit()