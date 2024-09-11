from awd_main.celery import app
from dataentry.utils import send_email_notification


@app.task
def send_email_task(
    mail_subject: str,
    message: str,
    to_email: str,
    attachment: str = None,
    email_id: str = None,
):
    try:
        send_email_notification(mail_subject, message, to_email, attachment, email_id)
    except Exception as e:
        raise e

    return "Emails Sent Successfully!"
