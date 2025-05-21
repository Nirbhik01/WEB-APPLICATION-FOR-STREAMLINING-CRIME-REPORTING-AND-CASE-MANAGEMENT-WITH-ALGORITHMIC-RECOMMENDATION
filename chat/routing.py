# chat/routing.py
from django.urls import re_path
from . import consumers

wsPattern = [
    re_path(r'casepage/(?P<case_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'/casepage/(?P<case_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]