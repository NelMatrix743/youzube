from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):

    user: models.OneToOneField[User] = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"  # lets you access it as user.profile.phone_number
    )
    phone_number: models.CharField = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"""
USERNAME: {self.user.username}
EMAIL: {self.user.email}
PHONE NUMBER: {self.phone_number}
"""
