from celery import Celery
from celery import shared_task
from .models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

@shared_task
def send_verification_email(user_id):
    
    user = User.objects.get(id=user_id)
    
    # django user k liy ek special token bnarah h
    token = default_token_generator.make_token(user)
    
    verification_link = (
        f"http://127.0.0.1:8000/api/accounts/verify-email/"
        f"?user_id={user_id}&token={token}"
    )
    
    subject = 'Verify you email'
    message = f"""Hi {user.username}, Welcome to our platform!
    
    Please verify your email address by clicking the link below:
    
    {verification_link}
    
    We're excited to have you with us. Your account has been successfully created.
    
    You can now log in and start exploring the platform.
    
    If you have any questions, feel free to contact our support team.
    
    Best regards,
    
    Our Platform Team"""
    
    send_mail(
        subject,
        message,
        None,
        [user.email],
        fail_silently = False
    )
    return f"Verification Email sent to {user.email}"