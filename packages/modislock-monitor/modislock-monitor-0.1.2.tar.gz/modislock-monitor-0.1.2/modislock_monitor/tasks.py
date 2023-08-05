# Async worker
from celery import Celery

# Database
from .database import Database, Settings, SettingsValues

# Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
from .config import load_config

# System calls
from subprocess import PIPE, Popen

# File operations
from shutil import copy2

config = load_config()
app = Celery('modis-mon', broker=config.CELERY_BROKER_URL)


@app.task
def reboot():
    args = ['systemctl', 'reboot']
    ret = Popen(args, stdout=PIPE, stderr=PIPE, timeout=60)
    ret.communicate()
    return {'message': 'Rebooting now'}


@app.task
def system_reset():
    with Database() as db:
        reset = db.session.query(SettingsValues)\
            .join(Settings, SettingsValues.settings_id_settings == Settings.id_settings)\
            .filter(Settings.settings_name == 'REGISTRATION').first()

        if reset is not None:
            reset.value = 'ENABLED'
            db.session.commit()

        args = ['supervisorctl', 'restart', 'admin:*']
        ret = Popen(args, stdout=PIPE, stderr=PIPE, timeout=60)
        ret.communicate()
        return {'message': 'Successfully reset registration'}


@app.task
def factory_reset():
    # 1. Reset database
    args = ['mysql', '-u', 'root', '-D', 'modislock']
    p = Popen(args, stdin=PIPE, stdout=PIPE)
    out, err = p.communicate('SOURCE /etc/modis/modislock_init.sql;\nexit\n'.encode(), timeout=30)
    print(out, err)

    # 2. Rename host
    with open('/etc/hostname', 'w') as f:
        f.write('modislock')

    # 3. Reset networking
    copy2('/etc/modis/interfaces.bu', '/etc/network/interfaces')

    # 4. Purge logs

    # 5. Reset passwords

    # 6. Restart system

    args = ['systemctl', 'reboot']
    ret = Popen(args, timeout=60)
    ret.communicate()
    return {'message': 'System reset to factory defaults'}


@app.task
def send_async_msg(message, server):
    """
    Send a message using SMTP
    :param from_address:
    :param kwargs:
    :return:
    """
    # Create a Container
    msg = MIMEMultipart()
    msg['Subject'] = message.subject
    msg['From'] = message.sender
    msg['To'] = message.destination
    msg.preamble = message.header

    # Add body
    body = MIMEText(message.body, 'html')
    msg.attach(body)

    send = smtplib.SMTP(server.address, server.port)
    # Add ttls
    send.ehlo()
    # Login
    send.login(server.user, server.password)
    # Send
    send.send_message(msg)
    # Quit
    send.quit()


__all__ = ['app', 'send_async_msg', 'reboot', 'system_reset', 'factory_reset']
