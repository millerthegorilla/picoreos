FROM python:latest
RUN useradd -m motioncore
RUN mkdir -p /home/motioncore/motion_files
RUN chown motioncore:motioncore /home/motioncore/motion_files
COPY ./motion_mail.py /home/motioncore/motion_mail.py
RUN chown motioncore:motioncore /home/motioncore/motion_mail.py
RUN chmod 0500 /home/motioncore/motion_mail.py
RUN su motioncore -c "cd && /usr/local/bin/python -m venv motioncore_venv"
RUN su motioncore -c "cd && . motioncore_venv/bin/activate && pip install --upgrade pip && pip install redmail"
CMD [ "sh", "-c", "cd && . motioncore_venv/bin/activate && python motion_mail.py" ]