import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shop.settings')
django.setup()

from django.conf import settings
from django.core.mail import EmailMessage, get_connection

print('Using EMAIL_HOST:', settings.EMAIL_HOST)
print('Using EMAIL_HOST_USER:', settings.EMAIL_HOST_USER)

try:
    conn = get_connection(backend=settings.EMAIL_BACKEND, username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
    msg = EmailMessage(subject='SMTP Test from Nexus', body='This is a test email sent by Django SMTP test script.', from_email=settings.DEFAULT_FROM_EMAIL, to=[settings.EMAIL_HOST_USER], connection=conn)
    sent = msg.send(fail_silently=False)
    print('Email send returned:', sent)
    print('Test email sent successfully.')
except Exception as e:
    print('Exception while sending email:')
    traceback.print_exc()
