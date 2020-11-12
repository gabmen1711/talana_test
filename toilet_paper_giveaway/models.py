from django.db import models
from django.utils import timezone


# For purpose of this test, database will be kept in SQLite
class Participants(models.Model):
    """
    Model for participants on toilet paper giveaway
    """
    name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=20, default="")
    subscribed_on = models.DateTimeField(default=timezone.now)


class Winners(models.Model):
    """
    Model to save winners for giveaway
    """
    participant_id = models.ForeignKey(Participants, on_delete=models.CASCADE)
    won_on = models.DateTimeField(default=timezone.now)
