from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('company', 'Company'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username