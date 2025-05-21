from django.db import models
from Case.models import Case
from userauths.models import Citizen as Ct, Investigator as It

class Message(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='chat_messages')
    sender_citizen = models.ForeignKey(Ct, on_delete=models.SET_NULL, null=True, blank=True)
    sender_investigator = models.ForeignKey(It, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        sender = self.sender_citizen.user_name if self.sender_citizen else self.sender_investigator.user_name
        return f"Message from {sender} in Case {self.case.case_id} at {self.timestamp}"
    
class Room(models.Model):
    room_id=models.AutoField(primary_key=True)
    room_name=models.ForeignKey(Case,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Room:-{self.room_id} , Item:- {self.room_name}"
# Create your models here.
