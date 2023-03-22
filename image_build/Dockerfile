FROM python:latest
RUN mkdir -p /var/lib/motion/files
RUN mkdir /init
COPY ./motion_mail.py /init/motion_mail.py
RUN pip install --upgrade pip
RUN pip install redmail
CMD [ "/init/motion_mail.py" ]
