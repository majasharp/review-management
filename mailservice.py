import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailService:
    def __init__(self, config):
        self.config = config
    
    def send_mail(self, message, receiver):
        recipients = self.config.get_extra_recipients()
        recipients.append(receiver)
        server = smtplib.SMTP_SSL(self.config.get_smtp_server())
        server.connect(self.config.get_smtp_server(), self.config.get_smtp_port())
        server.ehlo()
        server.login(self.config.get_sender_email(), self.config.get_sender_password())

        msg = MIMEText(message)
        msg['Subject'] = "Response to your review from Constella Review Management"
        msg['From'] = self.config.get_sender_email()
        msg['To'] = ", ".join(recipients)
        
        server.sendmail(self.config.get_sender_email(), recipients, msg.as_string())
        server.quit()