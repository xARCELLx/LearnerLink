from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            body=data['body'],
            subject=data['subject'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()
