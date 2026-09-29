from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Application(models.Model):

    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('interview', 'Interview'),
        ('selected', 'Selected'),
    )

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.candidate.username + " - " + self.job.title