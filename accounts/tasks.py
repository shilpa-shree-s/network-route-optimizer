from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import datetime


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_welcome_email(self, user_id):
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject="Welcome",
            message= f"Hi {user.username}, thanks for registering.",
            from_email="noreply@sv.com",
            recipient_list=[user.email]
        )
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task
def demo_beat():
    return f"executed at  {datetime.now()}"