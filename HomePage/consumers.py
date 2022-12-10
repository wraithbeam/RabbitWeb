import json
import zlib

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import Participant, MeetingParticipants, Meeting


class PersonChatConsumer(AsyncWebsocketConsumer):
    person = None
    meeting = None
    webcam_info = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await sync_to_async(self.delete)(self.person)
        await sync_to_async(self.process_meeting)(self.meeting)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            text_data_json = json.loads(text_data)
            image = text_data_json["webcam"]
            person_id = text_data_json["person"]
            self.person = person_id
            meeting = text_data_json["meeting"]
            self.meeting = meeting

            if image is not None:
                try:
                    participant = await Participant.objects.aget(id=person_id)
                    if participant.webcam_meta != image:
                        participant.webcam_meta = zlib.compress(image.encode())
                        await sync_to_async(participant.save)()
                        await sync_to_async(self.send_data)(meeting)
                except ObjectDoesNotExist:
                    print("Объект не сушествует")
                except MultipleObjectsReturned:
                    print("Найдено более одного объекта")

    def send_data(self, meeting_link):
        meeting = Meeting.objects.filter(link=meeting_link).get()
        data = {}
        for meeting_participant in MeetingParticipants.objects.filter(meeting=meeting.id).iterator():
            person = meeting_participant.person
            data[person.person.last_name + "_" + person.person.first_name] = {
                'mic': person.mic,
                'spk': True,
                'webcam': person.webcam,
                'mic_meta': person.mic_meta,
                'webcam_meta': (zlib.decompress(person.webcam_meta).decode()),
                'initials': person.person.last_name[0] + person.person.first_name[0]
            }
        async_to_sync(self.send)(json.dumps(data))

    def delete(self, id):
        Participant.objects.get(id=id).delete()

    def process_meeting(self, link):
        meeting = Meeting.objects.get(link=link)
        members = meeting.members
        if --members == 0:
            meeting.delete()

