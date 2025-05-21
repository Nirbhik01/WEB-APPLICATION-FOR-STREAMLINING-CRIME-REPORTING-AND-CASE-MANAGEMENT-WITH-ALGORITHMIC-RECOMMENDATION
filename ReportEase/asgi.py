# asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat.routing import wsPattern
from channels.sessions import SessionMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReportEase.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": 
        SessionMiddlewareStack(URLRouter(wsPattern)),
})
