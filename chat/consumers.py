import json
import base64
from django.core.files.base import ContentFile
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from Case.models import Case
from .models import Room, Message
from userauths.models import Citizen as Ct, Investigator as Iv
from ReportEaseApp.models import Notification
import redis
from asgiref.sync import sync_to_async

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@sync_to_async
def get_user_from_session(session):
    return {
        "user_type": session.get("user_type"),
        "user_id": session.get("user_id")
    }

class ChatConsumer(AsyncWebsocketConsumer):
    
    @sync_to_async
    def set_user_online(self):
        r.set(self.user_key, "online")

    @sync_to_async
    def set_user_offline(self):
        r.delete(self.user_key)

    @sync_to_async
    def is_user_online(self,user_key):
        return r.exists(user_key) == 1
    
    @sync_to_async
    def get_other_user_key(self):
        current_case = Case.objects.get(case_id=self.case_id)
        if self.user_type == "Citizen":
            return f"Investigator_{current_case.investigator.user_id}"
        elif self.user_type == "Investigator":
            return f"Citizen_{current_case.reporter.user_id}"
        return None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['case_id']
        self.case_id = self.scope['url_route']['kwargs']['case_id']
        
        user_data = await get_user_from_session(self.scope["session"])
        self.user_type = user_data["user_type"]
        self.user_id = user_data["user_id"]
        self.user_key = f"{self.user_type}_{self.user_id}"
        
        await self.set_user_online()
        
        await self.channel_layer.group_add(self.user_key, self.channel_name)
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.set_user_offline()
        await self.channel_layer.group_discard(self.user_key, self.channel_name)
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        self.close(code)
        
    async def receive(self,text_data):
        data_json = json.loads(text_data)
        event = {
            'type': 'send_message',
            'message': data_json,
        }
        
        await self.channel_layer.group_send(self.room_name, event)
        await self.create_message(data=data_json)
        
    async def send_message(self, event):
        data = event["message"]
        message_type = data.get("message_type", "text")
        
        if message_type == "image":
            # For image messages, we need to get the image URL from the database
            message = await self.get_message_url(data)
            response = {
                "sender": data["sender"],
                "sender_type": data["sender_type"],

                "message": message.image.url if message and message.image else data["message"],
                "message_type": "image"
            }
        else:
            response = {
                "sender": data["sender"],
                "sender_type": data["sender_type"],
                "message": data["message"],
                "message_type": "text"
            }
            
        await self.send(text_data=json.dumps({"message": response}))

        # Get other user's key
        other_user_key = await self.get_other_user_key()

        # Get this user's key
        sender_key = self.user_key

        # Only trigger notification logic if this is NOT the sender
        if self.user_key != other_user_key:
            if other_user_key and not await self.is_user_online(other_user_key):
                # Only the receiver and only if offline, create notification
                await self.create_notification(data)
            else:
                await self.mark_message_as_read(data)
        
    @database_sync_to_async
    def get_other_user(self):
        current_case = Case.objects.get(case_id=self.case_id)
        if self.user_type == "Citizen":
            return current_case.investigator.user_id
        elif self.user_type == "Investigator":
            return current_case.reporter.user_id
        return None
        
    @database_sync_to_async
    def create_message(self, data):
        get_case = Case.objects.get(case_id=data["room_name"])
        session = self.scope["session"]
        user_id = session.get("user_id")
        user_type = session.get("user_type") 
        sender_citizen = None
        sender_investigator = None
        
        if user_id and user_type == "Citizen":
            sender_citizen = Ct.objects.get(user_id=user_id)
        elif user_id and user_type == "Investigator":
            sender_investigator = Iv.objects.get(user_id=user_id)
        
        message_type = data.get("message_type", "text")
        content = data["message"]
        
        if message_type == "image" and content.startswith("data:image"):
            # Handle image upload
            format, imgstr = content.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'chat_image_{get_case.case_id}_{user_id}.{ext}')
            
            new_message = Message(
                case=get_case,
                sender_citizen=sender_citizen,
                sender_investigator=sender_investigator,
                content="[Image]",  # Placeholder text for image messages
                message_type="image",
                image=image_data,
                is_read=False
            )
        else:
            # Handle text message
            if content.strip() != "":
                new_message = Message(
                    case=get_case,
                    sender_citizen=sender_citizen,
                    sender_investigator=sender_investigator,
                    content=content,
                    message_type="text",
                    is_read=False
                )
        
        if new_message:
            new_message.save()
            # For image messages, update the content with the image URL
            if message_type == "image":
                new_message.content = new_message.image.url
                new_message.save()

    @database_sync_to_async
    def mark_message_as_read(self, data):
        get_case = Case.objects.get(case_id=data["room_name"])
        Message.objects.filter(
            case=get_case,
            is_read=False
        ).update(is_read=True)
        
    @database_sync_to_async
    def create_notification(self, data):
        get_case = Case.objects.get(case_id=data["room_name"])
        session = self.scope["session"]
        user_id = session.get("user_id")
        user_type = session.get("user_type")
        
        # Get unread message count
        unread_count = Message.objects.filter(
            case=get_case,
            is_read=False
        ).count()
        
        # Determine recipient
        if user_type == "Citizen":
            recipient = get_case.investigator
            notification, created = Notification.objects.get_or_create(
                belongs_to_investigator=recipient,
                case=get_case,
                status='UNREAD',
                defaults={
                    'message': f'You have {unread_count} unread messages in case {get_case.case_title} from {get_case.reporter.user_name}',
                }
            )
            if not created:
                notification.message = f'You have {unread_count} unread messages in case {get_case.case_title} from {get_case.reporter.user_name}'
                notification.save()
        else:
            recipient = get_case.reporter
            notification, created = Notification.objects.get_or_create(
                belongs_to_citizen=recipient,
                case=get_case,
                status='UNREAD',
                defaults={
                    'message': f'You have {unread_count} unread messages in case {get_case.case_title} from {get_case.investigator.user_name}',
                }
            )
            if not created:
                notification.message = f'You have {unread_count} unread messages in case {get_case.case_title} from {get_case.investigator.user_name}'
                notification.save()
                
    @database_sync_to_async
    def get_message_url(self, data):
        try:
            return Message.objects.filter(
                case_id=data["room_name"],
                sender_citizen__user_id=data["sender"] if data.get("sender_type") == "Citizen" else None,
                sender_investigator__user_id=data["sender"] if data.get("sender_type") == "Investigator" else None,
                message_type="image"
            ).latest('timestamp')
        except Message.DoesNotExist:
            return None
                