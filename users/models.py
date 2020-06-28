from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class CardClass(models.Model):
    name = models.CharField(max_length=64)
    cardClass = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Status(models.Model):
    status = models.CharField(max_length=64)
    cardClass = models.ForeignKey('CardClass', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status}"

class Tag(models.Model):
    tag = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.tag}"

#Will have to decide how to limit many to many
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=64)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='manager')
    status = models.ForeignKey('Status', on_delete=models.PROTECT,)
    contributors = models.ManyToManyField(User, related_name='contributor', blank=True,)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True,)

    def __str__(self):
        return f"{self.name} by {self.manager}"
