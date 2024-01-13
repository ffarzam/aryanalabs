from celery import shared_task

from .utils import send_email


@shared_task
def send_login_notification(users_email):

    email_body = "you just login"
    subject = "login notification"
    email_data = {"email_body": email_body, "to_email": [users_email], "email_subject": subject}
    send_email(email_data)
