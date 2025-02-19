from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=200)
    user_address = models.CharField(max_length=400)
    user_email = models.EmailField()
    user_phone_number = models.IntegerField(max_length=10)

    def __init__(self):
        return f"{self.user_name}"

class Investigator(models.Model):
    
    pass

# Create your models here.
