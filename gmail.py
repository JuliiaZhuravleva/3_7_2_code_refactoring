import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Gmail:
    def __init__(self, **login_data):
        self.GMAIL_SMTP = "smtp.gmail.com"
        self.GMAIL_IMAP = "imap.gmail.com"
        self.login = login_data['login']
        self.password = login_data['password']

    def send_message(self, **mail_to_send):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(mail_to_send['recipients'])
        msg['Subject'] = mail_to_send['subject']
        msg.attach(MIMEText(mail_to_send['message']))
        ms = smtplib.SMTP(self.GMAIL_SMTP, 587)
        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(msg=msg.as_string(), from_addr=self.login, to_addrs=mail_to_send['recipients'])

        ms.quit()

    def receive_message(self, header=None):
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail.login(self.login, self.password)

        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.search(None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.fetch(latest_email_uid, '(RFC822)')
        raw_email = data[0][1].decode('ascii')
        email_message = self.parse_email(email.message_from_string(raw_email))

        mail.logout()

        return email_message

    @staticmethod
    def parse_email(email_message):
        subject = email_message['Subject']
        sender = email_message['From']
        if email_message.is_multipart():
            body = []
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    body.append(part.get_payload(decode=True).decode())
            text = '\n'.join(body)
        else:
            text = email_message.get_payload(decode=True).decode()

        return {'subject': subject, 'sender': sender, 'text': text}
