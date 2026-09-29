from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):

    candidate = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    resume_file = models.FileField(
        upload_to='resumes/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    extracted_text = models.TextField(
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.candidate.username