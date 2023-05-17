from enum import Enum
import threading
import smtplib
import ssl
from email.message import EmailMessage
from threading import Thread
import json


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


class Logger:
    def __init__(self, min_log_level=LogLevel.DEBUG):
        self.min_log_level = min_log_level
        self.log_targets = []
        self.lock = threading.Lock()
        self.sender = Sender()
        self.receivers_emails = []
        self.json = self.read_data()
        self.recievers_json = self.json['log_levels']
        
        for email in self.recievers_json.values():
            self.receivers_emails.append(email)
        
        self.sender_cred = self.json['sender']
        
        self.console_target = ConsoleLogTarget()
        self.add_log_target(self.console_target)

    def read_data(self):
        with open('data.json', 'r') as file:
            # Step 3: Read the file content
            content = file.read()
            # Step 4: Parse the JSON
            data = json.loads(content)
        return data
        
    def add_log_target(self, log_target):
        self.log_targets.append(log_target)

    def remove_log_target(self, log_target):
        self.log_targets.remove(log_target)

    def _log(self, message, log_level=LogLevel.INFO):
        if log_level.value < self.min_log_level.value:
            return
        with self.lock:
            for i, log_target in enumerate(self.log_targets):
                log_target.log(message, log_level)
                self.sender.send_email(self.receivers_emails[log_level.value - 1], message, self.sender_cred)
    
    def log(self, message, log_level=LogLevel.INFO):
        threading.Thread(target=self._log, args=[message, log_level]).start()


class Sender:
    def send_email(self, email_receiver, message, sender):
        email_sender = sender['email']
        #Enable 2-step verification and provide the generated password instead of the account password in the code.
        email_password = sender['password']
        # Set the subject and body of the email
        subject = 'Logger'
        body = message

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

#         print(f"Message -> {message} <- send to -> {email} <- email.") 
         
class LogTarget:
    def log(self, message, log_level):
        raise NotImplementedError("Subclasses must implement log method.")


class ConsoleLogTarget():
    def log(self, message, log_level):
        print(f"[{log_level.name}] {message}")




