from django.db import models
from datetime import date
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    mobile_number= models.CharField(max_length=15, blank=True)
    date_of_birth=models.DateField(null=True, blank=True)
    profile_picture= models.ImageField(
        upload_to='profile_pics',
        null=True,
        blank=True
    )

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today= date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )