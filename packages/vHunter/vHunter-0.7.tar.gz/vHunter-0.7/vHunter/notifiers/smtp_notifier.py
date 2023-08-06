import smtplib
import base64
from email.mime.text import MIMEText
from pprint import pformat

from vHunter.utils import Config


class SmtpNotifier:
    def __init__(self, domain, port=587, sender=None):
        self.mail = smtplib.SMTP(domain, port)
        self.sender = sender

    def prepare_message(self, receivers, subject, body, sender=None):
        message = MIMEText(body)
        # if sender is not None:
        message['To'] = ', '.join(receivers)
        message['Subject'] = subject
        #message['Content-Type'] = 'text/plain'
        return message.as_string()

    def send_msg(self, receives, subject, body):
        self.mail.ehlo()
        self.mail.starttls()
        self.mail.ehlo()
        self.mail.login(self.username, self.password)
        message = self.prepare_message(receives, subject, body, self.sender)
        self.mail.sendmail('notify@vhunter.tk', receives, message)
        self.mail.quit()


class MailNotifier(SmtpNotifier):
    def __init__(self):
        self.config = Config()['mail_notifier']
        self.username = self.config['account']
        self.password = base64.b64decode(self.config['pass']).decode()
        super().__init__(
            self.config['domain'],
            sender=self.config['account'],
        )

    '''
       vulnerabilities = {
        'ip': ['list', 'of', 'vulnerable', 'apps']
       }
    '''
    def send_msg(self, receivers, vulnerabilities):
        subject = self.config['subject'] % (
            sum(map(lambda x: len(x), vulnerabilities.values())),
            len(vulnerabilities.keys())
        )
        body = self.config['body'] % pformat(vulnerabilities, indent=4, width=80).replace('\n', '\r\n')
        super().send_msg(receivers, subject, body)
