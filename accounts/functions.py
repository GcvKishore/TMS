from django.core.mail import send_mail
from django.conf import settings


def emailPasswordResetLink(token, email, host):
    protocol = 'https'
    if settings.DEBUG:
        protocol = 'http'

    subject = 'Your forget password link'
    message = f'Hi,\n click on the link to reset your password {host}/account/change-password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
