from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def sleepy(duration):
    sleep(duration)
    return None



@shared_task
def send_mail_token_task(email,token):
    print(email)
    print(token)
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list, fail_silently=False)
    return None
