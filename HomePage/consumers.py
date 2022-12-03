import copy
import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import Participant, MeetingParticipants, Meeting

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            text_data_json = json.loads(text_data)
            image = text_data_json["webcam"]
            person_id = text_data_json["person"]
            meeting = text_data_json["meeting"]
            if image:
                try:
                    participant = await Participant.objects.aget(person=person_id)
                    participant.webcam_meta = image
                    await sync_to_async(participant.save)()
                except ObjectDoesNotExist:
                    print("Объект не сушествует")
                except MultipleObjectsReturned:
                    print("Найдено более одного объекта")
            await self.send_data(meeting)

    async def send_data(self, meeting_link):
        meeting = await Meeting.objects.filter(link=meeting_link).aget()
        data = {}
        async for meeting_participant in MeetingParticipants.objects.filter(meeting=meeting.id):
            person = await Participant.objects.aget(id=meeting_participant.person_id)
            data[person] = {
                'mic': person.mic,
                'spk': True,
                'webcam': person.webcam,
                'mic_meta': person.mic_meta,
                'webcam_meta': person.webcam_meta
            }
        await self.send(text_data=json.dumps(data))
