#!/usr/bin/python3

import hashlib
import os
import sys
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

if __name__ == "__main__":
    filepath = Path(os.getenv('MOTION_FILE_PATH'))
    filename = filepath.name
    host=f"{os.getenv('MOTION_EMAIL_HOST')}",
    port=f"{os.getenv('MOTION_EMAIL_PORT')}",
    user_address=f"{os.getenv('MOTION_EMAIL_USERNAME')}",
    password=f"{os.getenv('MOTION_EMAIL_PASS')}",

    sha256_hash = hashlib.sha256()
    with filepath.open('rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload((attachment).read())
        for byte_block in iter(lambda: attachment.read(4096),b""):
            sha256_hash.update(byte_block)
    
    checksum = sha256_hash.hexdigest()
    
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    
    subject = "A new file has been generated by motioncore"
    body = f"<h2><style='color:red'>Motion detected!</style></h2><br><h3>Motion has been detected.<br>Sha256sum checksum of attachment {filename} is {checksum}</h3>"

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = user_address
    message['To'] = user_address
    html_part = MIMEText(body, 'html')
    message.attach(html_part)
    message.attach(part)

    sslcontext = ssl.create_default_context()
    server = smtplib.SMTP_SSL(host, 465, context=sslcontext)
    server.login(user_address, password)
    server.sendmail(, user_address, message.as_string())
    server.quit()