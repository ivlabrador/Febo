import smtplib

from django.template.loader import render_to_string

from config import settings as s
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from django.conf import settings
#settings.configure()
# Create your tests here.


def send_email():
    try:
        mailServer = smtplib.SMTP(s.EMAIL_HOST, s.EMAIL_PORT)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(s.EMAIL_HOST_USER, s.EMAIL_HOST_PASSWORD)
        print('conectadoooooo')

        #Construccion del mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = s.EMAIL_HOST_USER
        mensaje['To'] = 'ilabrador@outlook.com'
        mensaje['Subject'] = 'Febo Authentication System'

        #mailServer.sendmail(s.EMAIL_HOST_USER, 'ilabrador@outlook.com', mensaje.as_string())
        print('aca')
        content = render_to_string('reset_password_email.html', {'user': 'aa'})
        mensaje.attach(MIMEText(content, 'html'))
        print('content')
        mailServer.sendmail(s.EMAIL_HOST_USER,
                            'ilabrador@outlook.com',
                            mensaje.as_string())
        print('correo enviado')
    except Exception as e:
        print('exception')
        print(e)

send_email()