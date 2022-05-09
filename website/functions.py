from django.core.mail import send_mail
from django.conf import settings


def sendUserCopy(post):
    subject = f"Reg. Your Tutest Support Request {post['subject']}"
    message = f"""
Dear User,

Thank you for contacting our support team. Below is the copy of your request.

Category: {post['subject']}
Message:
{post['message']}

A member of our support staff will respond yo your request as soon as possible.

Regards,
Support Team,
Tutest
"""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [post['email']]
    send_mail(subject, message, email_from, recipient_list)
    return True
