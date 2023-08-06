# coding: utf-8
# Flask
from flask import (render_template, Blueprint, send_file, request, current_app)
from flask_security import login_required

# Database
from ..models import (db, Events, SettingsValues, Settings)
from sqlalchemy.exc import InternalError, IntegrityError

# File handing
import gzip
import shutil

# OS
from datetime import datetime
import os
from subprocess import Popen, PIPE, TimeoutExpired
import re
from io import BytesIO
from pathlib import Path

# Async
from ..tasks import send_async_command


bp = Blueprint('settings_backup', __name__)


def allowed_file(filename):
    """Allowed file extension types that will be accepted on restore

    :param str filename:
    :return str filename:
    """
    ALLOWED_EXTENSIONS = set(['mod', 'zip'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/settings/backup/run_backup', methods=['POST'])
@login_required
def backup_db():
    """Backs up database from dump, compresses and uploads to client

    :return file db_backup: Returns a compressed database file with timestamp and suffix of .mod
    """
    db_config = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    p = re.compile(r'[/]{2}([\w]+):([\w]+)@([a-zA-Z0-9._\-]+)/([\w]+)')
    m = p.search(db_config)
    # args = ['mysqldump', '-u', m.group(1), '-p' + m.group(2), '-h', m.group(3), '--databases', m.group(4)]
    args = ['mysqldump', '-u', 'root', '-h', m.group(3), '--databases', m.group(4)]

    p1 = Popen(args, stdout=PIPE)
    p2 = Popen('gzip', stdin=p1.stdout, stdout=PIPE)
    cmd_data = p2.communicate(timeout=60)[0]

    current_app.logger.info('Database is backed up in the pipe, now sending to stream')

    last_bu = SettingsValues.query.join(Settings, SettingsValues.settings_id_settings == Settings.id_settings) \
        .filter(Settings.settings_name == 'LAST_BACKUP') \
        .first()

    last_bu.value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.commit()

    return send_file(BytesIO(cmd_data),
                     attachment_filename='lock' + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.mod',
                     as_attachment=True)


@bp.route('/settings/backup/run_restore', methods=['GET', 'POST'])
@login_required
def restore_db(filename):
    """Restores database from downloaded file

    :param str filename:
    :return bool result: True / False based on operation results
    """
    rest_file = Path(filename)

    if rest_file.is_file():
        os.chdir(str(rest_file.parent))
        try:
            with gzip.open(rest_file.name, 'rb') as f:
                with open('restore.sql', 'wb') as f_out:
                    shutil.copyfileobj(f, f_out)
        except Exception as e:
            return False

        db_config = current_app.config.get('SQLALCHEMY_DATABASE_URI')
        p = re.compile(r'[/]{2}([\w]+):([\w]+)@([a-zA-Z0-9._\-]+)/([\w]+)')
        m = p.search(db_config)
        # args = ['mysql', m.group(4), '-u', m.group(1), '-p' + m.group(2), '-h', m.group(3)]
        args = ['mysqldump', '-u', 'root', '-h', m.group(3), '--databases', m.group(4)]

        proc = Popen(args, stdin=PIPE, stdout=PIPE)

        db.session.remove()

        try:
            outs, errs = proc.communicate('SOURCE restore.sql;\nexit\n'.encode(), timeout=30)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        finally:
            os.remove('restore.sql')
            os.remove(rest_file.name)

        return True
    else:
        current_app.logger.info('File provided for database restore is not valid')
        return False


@bp.route('/settings/backup', methods=['GET', 'POST'])
@login_required
def backup_settings():
    """Backup endpoint

    :return html settings_backup.html:
    """
    if request.method == 'POST':
        if request.form['action'] == 'reboot':
            args = ['systemctl', 'reboot']
            send_async_command.delay(args)
        elif request.form['action'] == 'purge':
            Events.query.delete()
            try:
                db.session.commit()
            except (InternalError, IntegrityError):
                current_app.logger.debug('Error occurred when purging events from database')
            else:
                current_app.logger.info('Purged all events from database')
        return render_template('settings_backup/system_rebooting.html', domain=current_app.config.get('SITE_DOMAIN'))
    else:
        try:
            last_bu = SettingsValues.query.join(Settings, SettingsValues.settings_id_settings == Settings.id_settings) \
                .filter(Settings.settings_name == 'LAST_BACKUP') \
                .first()
            back_age = (datetime.now() - datetime.strptime(last_bu.value, '%Y-%m-%d %H:%M:%S')).days
        except AttributeError:
            back_age = 0

        return render_template('settings_backup/settings_backup.html', backup_age=back_age)
