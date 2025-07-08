import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Hotel


def generate_randon_token():
    return str(uuid.uuid4())


def send_email_token(email, token):
    subject = "Verify you email"
    message = f"""Hi Please verify your email using below link
    http://127.0.0.1:8000/account/verify-token/{token}
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def send_otp_to_email(email, otp):
    subject = "OTP for Login"
    message = f"""Hi Use OTP to login
    <b>{otp}</b>
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def generate_slug(hotel_name):
    slug = slugify(hotel_name) + "-" + str((uuid.uuid4())).split('-')[0]
    if Hotel.objects.filter(hotel_slug=slug).exists():
        generate_slug(hotel_name)
    return slug
