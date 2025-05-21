import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from Case.models import Case
from .models import Room,Message
from userauths.models import Citizen as Ct, Investigator as Iv

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['case_id']
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        self.close(code)
        
    async def receive(self,text_data):
        data_json = json.loads(text_data)
        print('receive ma cha---',data_json)
        event = {
            'type': 'send_message',
            'message': data_json,
        }
        
        await self.channel_layer.group_send(self.room_name, event)
        
    async def send_message(self, event):
        data = event["message"]
        # print('send ma cha---',data)
        # await self.create_message(data=data)
        response = {
                "sender":data["sender"],
                "message":data["message"],
            }
        await self.send(text_data=json.dumps({"message":response})) 
        
    @database_sync_to_async
    def create_message(self, data):
        get_case=Case.objects.get(case_id=data["room_name"])
        session = self.scope["session"]
        user_id = session.get("user_id")
        user_type = session.get("user_type") 
        sender_citizen = None
        sender_investigator = None
        if user_id and user_type == "Citizen":
            sender_citizen = Ct.objects.get(user_id=user_id)
        elif user_id and user_type == "Investigator":
            sender_investigator = Iv.objects.get(user_id=user_id)
        
        if data["message"].strip() != "":
            new_message = Message(
                case=get_case,
                sender_citizen=sender_citizen,
                sender_investigator=sender_investigator,
                content=data["message"]
            )
            new_message.save()
                
            
            
        