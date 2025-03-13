FROM python:latest
RUN useradd -m motioncore
RUN apt-get update && apt-get install -y motion
RUN mkdir -p /home/motioncore/motion_files
RUN chown motioncore:motioncore /home/motioncore/motion_files
COPY ./motion_mail.py /usr/local/sbin/motion_mail.py
RUN chown root:motioncore /usr/local/sbin/motion_mail.py
RUN chmod 0550 /usr/local/sbin/motion_mail.py
COPY ./motion.conf /etc/motion/motion.conf
RUN chown root:video /etc/motion/motion.conf
RUN chmod 0550 /etc/motion/motion.conf
COPY ./motion_start.py /usr/local/sbin/motion_start.py
RUN chown root:motioncore /usr/local/sbin/motion_start.py
RUN chmod 0550 /usr/local/sbin/motion_start.py
COPY ./p-boot_start /etc/network/if-up.d/p-boot_start
RUN chown root:root /etc/network/if-up.d/p-boot_start
RUN chmod 0550 /etc/network/if-up.d/p-boot_start
COPY ./source.sh /usr/local/sbin/source.sh
RUN chown root:root /usr/local/sbin/source.sh
RUN chmod 0550 /usr/local/sbin/source.sh
# RUN su motioncore -c "cd && /usr/local/bin/python -m venv motioncore_venv"
# RUN su motioncore -c "cd && . motioncore_venv/bin/activate && pip install --upgrade pip && pip install redmail"
# CMD [ "sh", "-c", "cd && . motioncore_venv/bin/activate && python motion_mail.py" ]