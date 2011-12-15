from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()

class EventStat(models.Model):
    event = models.ForeignKey(Event)
    invited = models.PositiveIntegerField()
    attending = models.PositiveIntegerField()
    maybe = models.PositiveIntegerField()
    time = models.DateTimeField()

