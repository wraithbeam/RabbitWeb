import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class MeetingConsumer(AsyncWebsocketConsumer):
    initials = {}
    webcams = {}

    async def disconnect(self, code):
        await sync_to_async(self.initials.clear)()
        await sync_to_async(self.webcams.clear)()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            text_data_json = json.loads(text_data)
            person_name = text_data_json["person_name"]
            image = text_data_json["webcam"]
            person_initials = text_data_json['person_initials']

            self.webcams[person_name] = image
            self.initials[person_name] = person_initials

            await self.send_data()

    async def send_data(self):
        data = {}
        for key, value in self.webcams.items():
            data[key] = {
                'webcam_meta': value,
                'initials': self.initials[key]
            }
        await self.send(json.dumps(data))
