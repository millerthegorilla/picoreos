#!/usr/bin/env/ python

import os
from redmail import EmailSender
from pathlib import Path
import sys
import hashlib
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

filepath = Path(os.getenv('MOTION_FILE_PATH'))
filename = filepath.name

sha256_hash = hashlib.sha256()
with filepath.open('rb') as f:
   for byte_block in iter(lambda: f.read(4096),b""):
       sha256_hash.update(byte_block)

checksum = sha256_hash.hexdigest()

# Configure an email sender
email = EmailSender(
    host=f"{os.getenv('MOTION_EMAIL_HOST')}", port=f"{os.getenv('MOTION_EMAIL_PORT')}",
    username=f"{os.getenv('MOTION_EMAIL_USERNAME')}", password=f"{os.getenv('MOTION_EMAIL_PASS')}",
    use_starttls=True
)

# Send an email
email.send(
    sender=f"{os.getenv('MOTION_EMAIL_SENDER')}",
    receivers=[f"{os.getenv('MOTION_EMAIL_RECEIVER')}"],
    subject="A new motion file has been generated",
    text=f"The checksum is {checksum}",
    attachments={
        filename: filepath,
    }
)