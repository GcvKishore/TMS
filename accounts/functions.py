from django.core.mail import send_mail
from django.conf import settings


def emailPasswordResetLink(token, user, host):
    protocol = 'https'
    if settings.DEBUG:
        protocol = 'http'

    subject = 'Your tutest account password reset link'
    message = f"Hi {user.first_name} {user.last_name},\n\nclick on the link below to reset your password.\nReset " \
              f"Password link: {protocol}://{host}/account/change-password/{token}\n\nRegards,\nTutest Team "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)
    return True
