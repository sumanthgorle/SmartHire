from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):

    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=100
    )

    description = models.TextField()

    required_skills = models.TextField()

    location = models.CharField(
        max_length=100
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title