from django.contrib.auth import get_user_model
from django.db import close_old_connections
from urllib.parse import parse_qs
from channels.middleware.base import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token):
    try:
        # Replace this with your actual user authentication logic
        return User.objects.get(auth_token=token)
    except User.DoesNotExist:
        return AnonymousUser()

class CustomAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Get token from query string or cookies
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        scope["user"] = await get_user_from_token(token)
        close_old_connections()
        return await super().__call__(scope, receive, send)
