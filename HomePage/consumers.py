import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import Participant, MeetingParticipants, Meeting

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            image = text_data_json["webcam"]
            person_id = text_data_json["person"]
            meeting = text_data_json["meeting"]
            if image:
                try:
                    participant = Participant.objects.get(person=person_id)
                    participant.webcam_meta = image
                    participant.save()
                except ObjectDoesNotExist:
                    print("Объект не сушествует")
                except MultipleObjectsReturned:
                    print("Найдено более одного объекта")
            self.send_data(meeting)

    def send_data(self, meeting_link):
        meeting = Meeting.objects.filter(link=meeting_link)
        meeting_participants = MeetingParticipants.objects.filter(meeting=meeting[0].id)
        data = {}
        for meeting_participant in meeting_participants:
            person = Participant.objects.get(id=meeting_participant.person.id)
            data[person.person.first_name + "_" + person.person.last_name] = {
                'mic': person.mic,
                'spk': True,
                'webcam': person.webcam,
                'mic_meta': person.mic_meta,
                'webcam_meta': person.webcam_meta
            }
        self.send(text_data=json.dumps(data))
