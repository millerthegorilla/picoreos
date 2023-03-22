#!/usr/local/bin/python

import os
from redmail import EmailSender
from pathlib import Path
import sys
import hashlib
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

filepath = Path(os.getenv('MOTION_FILEPATH'))
filename = filepath.name

sha256_hash = hashlib.sha256()
with filepath.open('rb') as f:
   for byte_block in iter(lambda: f.read(4096),b""):
       sha256_hash.update(byte_block)

checksum = sha256_hash.hexdigest()

# Configure an email sender
email = EmailSender(
    host="smtp.gmail.com", port=587,
    username="jamesstewartmiller@gmail.com", password=f"{os.getenv('MOTION_PASS')}",
    use_starttls=True
)

# Send an email
email.send(
    sender="corvid@home.james",
    receivers=["jamesstewartmiller@gmail.com"],
    subject="A new motion file has been generated",
    text=f"The checksum is {checksum}",
    attachments={
        filename: filepath,
    }
)
