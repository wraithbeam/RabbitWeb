from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Meeting:
    link = models.CharField(max_length=30)
    members = models.IntegerField(default=0)
    admin = models.ForeignKey("Participant", on_delete=models.CASCADE)


class Participant:
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    mic = models.BooleanField(default=False)
    spk = models.BooleanField(default=True)
    webcam = models.BooleanField(default=False)
