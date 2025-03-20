# motioncore
provisioning for coreos rpi4 motion webcam server
mit license

# dependencies
  python3-rpm on the host and pip install rpm in the prefix.
# optional
  coreos-installer
  
ansible-vault encrypt_string --ask-vault-pass 'gmail_password_here' --name 'motion_email_password'

.env contents
```
MOTION_EMAIL_HOST="smtp.gmail.com"
MOTION_EMAIL_ADDRESS="jamesstewartmiller@gmail.com"
MOTION_EMAIL_PASSWORD="\\\$ANSIBLE_VAULT;1.1;AES256\n39653...\n....\n653534643561"
```

Todo -- make a vault file for the motion_email_password
