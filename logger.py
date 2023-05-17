from enum import Enum
import threading
import smtplib
import ssl
from email.message import EmailMessage
from threading import Thread


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
        self.receivers_emails = ['mariam.harutyunyan.ca@gmail.com', 
                                 'edik.mughdusyan.ca@gmail.com',  
                                 'mariam.harutyunyan.ca@gmail.com',
                                 'armtatevik2015@gmail.com']
        
        self.console_target = ConsoleLogTarget()
        self.add_log_target(self.console_target)

    def add_log_target(self, log_target):
        self.log_targets.append(log_target)

    def remove_log_target(self, log_target):
        self.log_targets.remove(log_target)

    def _log(self, message, log_level=LogLevel.INFO):
        if log_level.value < self.min_log_level.value:
            return
        print('aaa')
        with self.lock:
            for i, log_target in enumerate(self.log_targets):
                log_target.log(message, log_level)
                self.sender.send_email(self.receivers_emails[log_level.value - 1], message)
    
    def log(self, message, log_level=LogLevel.INFO):
        print('aaa')
        threading.Thread(target=worker, args=[message, log_level], daemon=True).start()


class Sender:
    def send_email(self, email_receiver ,message):
        email_sender = 'tatev.avetisyan.ca@gmail.com'
        #Enable 2-step verification and provide the generated password instead of the account password in the code.
        email_password = 'sooyejpqmvevosgm'
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




