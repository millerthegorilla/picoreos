# motioncore
provisioning for coreos rpi4 motion webcam server
mit license

ansible-vault encrypt_string --ask-vault-pass 'gmail_password_here' --name 'motion_email_pass'

.env contents
```
MOTION_EMAIL_HOST="smtp.gmail.com"
MOTION_EMAIL_ADDRESS="jamesstewartmiller@gmail.com"
MOTION_EMAIL_PASS="!vault |
        $ANSIBLE_VAULT;1.1;AES256
        39653...
        ....653534643561"
```