# Automatic sending notification email module

import ssl, smtplib
from email.message import EmailMessage

class EmailController:
    def __init__(self, From, Host, Port, Password) -> None:
        self.emo = EmailMessage()
        self.From = From
        self.Host = Host
        self.Port = Port
        self.Password = Password
        self.Context = ssl.create_default_context()
        
    def create(self, To, Subject, Body) -> None:
        """
        Function for creating email
        Subject: Title
        Body: Email content
        """
        self.emo['To'] = To
        self.emo['subject'] = Subject
        self.emo.set_content(Body)
        
    def create_attachment(self, file_path):
        """
        Function for setting attachments
        file_path: Path to the attachments
        """
        with open(file_path, 'rb') as file:
            file_data = file.read()
            file_name = file.name
        self.emo.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    def send(self) -> None:
        """
        Function for sending email
        """
        with smtplib.SMTP_SSL(self.Host, self.Port, context=self.Context) as smtp:
            self.emo['From'] = self.From
            smtp.login(self.From, self.Password)
            smtp.sendmail(self.From,  self.emo['To'], self.emo.as_string())
            smtp.quit()