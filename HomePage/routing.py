# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/meeting/(?P<room_name>\S+)/(?P<persone>\S+)/$", consumers.ChatConsumer.as_asgi()),
]