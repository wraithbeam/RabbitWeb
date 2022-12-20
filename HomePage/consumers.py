import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class MeetingConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None
        self.initials = {}
        self.webcams = {}

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await sync_to_async(self.initials.clear)()
        await sync_to_async(self.webcams.clear)()
        # Leave room
        await self.channel_layer.group_send(self.room_group_name, {"type": "delete"})
        await self.channel_layer.group_send(self.room_group_name, {"type": "delete"})
        await self.channel_layer.group_send(self.room_group_name, {"type": "delete"})
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            text_data_json = json.loads(text_data)
            type = text_data_json["type"]
            if type == 'webcam':
                person_name = text_data_json["person_name"]
                image = text_data_json["webcam"]
                person_initials = text_data_json['person_initials']

                self.webcams[person_name] = image
                self.initials[person_name] = person_initials

                await self.send_data()
            elif type == 'message':
                await self.channel_layer.group_send(
                    self.room_group_name, text_data_json)
            elif type == 'sound':
                await self.channel_layer.group_send(
                    self.room_group_name, text_data_json)

    async def send_data(self):
        data = {"type": "webcam", "content": {}}
        for key, value in self.webcams.items():
            data["content"][key] = {
                'webcam_meta': value,
                'initials': self.initials[key]
            }
        await self.channel_layer.group_send(
            self.room_group_name, data)

    async def webcam(self, event):
        await self.send(text_data=json.dumps(event))

    async def delete(self, event):
        await self.send(text_data=json.dumps(event))

    async def message(self, event):
        await self.send(text_data=json.dumps(event))

    async def sound(self, event):
        await self.send(text_data=json.dumps(event))
