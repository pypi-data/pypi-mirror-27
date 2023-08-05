from flask import current_app, render_template
from flask_mail import Message
from modislock_webservice.tasks import send_async_email


def _msg_to_dict(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    msg = Message(
        subject=app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[to]
    )

    msg.body = render_template('email_templates/' + template + '.txt', **kwargs)
    msg.html = render_template('email_templates/' + template + '.html', **kwargs)

    return msg.__dict__


def send_email(to, subject, template, **kwargs):
    """Send email through async task

    :param to:
    :param subject:
    :param template:
    :param kwargs:

    :return:
    """
    send_async_email.delay(_msg_to_dict(to, subject, template, **kwargs))
