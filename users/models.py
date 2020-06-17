from django.db import models
from django.conf import settings

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=64)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    PLANNING = 'PL'
    QUEUED = 'QD'
    IN_PROGRESS = 'IP'
    COMPLETED = 'CO'
    ABANDONED = 'AB'
    STATUS_CHOICES = [
        (PLANNING, 'Planning'),
        (QUEUED, 'QD'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (ABANDONED, 'Abandoned'),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PLANNING,)
