from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Meeting(models.Model):
    link = models.CharField(max_length=30)
    members = models.IntegerField(default=0)
    admin = models.ForeignKey("Participant", on_delete=models.CASCADE)

    def __str__(self):
        return "Meeting " + self.admin.person.last_name + " " + self.admin.person.first_name


class Participant(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    mic = models.BooleanField(default=False)
    spk = models.BooleanField(default=True)
    webcam = models.BooleanField(default=False)
    mic_meta = models.TextField(default="")
    webcam_meta = models.BinaryField()

    def __str__(self):
        return self.person.last_name + " " + self.person.first_name


class MeetingParticipants(models.Model):
    person = models.ForeignKey(Participant, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return self.person.__str__() + " in " + self.meeting.__str__()
