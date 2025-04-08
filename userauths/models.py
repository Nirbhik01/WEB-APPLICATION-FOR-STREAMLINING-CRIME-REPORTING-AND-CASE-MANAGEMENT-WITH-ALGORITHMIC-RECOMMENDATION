from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.text import slugify
from django.core.files.storage import default_storage
import os

def citizen_profile_pic_path(instance, filename): #instance represents the current class object being used
    ext = filename.split('.')[-1]  # Get file extension (png, jpg, etc.)
    email_slug = slugify(instance.user_email.split('.')[0])  # Sanitize email
    new_filename = f"{email_slug}.{ext}"  # Create new filename
    return os.path.join('ReportEaseApp/ProfilePics/Citizen', new_filename)

class Citizen(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=200)
    user_address = models.CharField(max_length=400)
    user_email = models.EmailField()
    user_phone_number = models.IntegerField()
    user_profile_picture = models.ImageField(upload_to = citizen_profile_pic_path,null=True, blank=True)
    user_type=models.CharField(max_length=15,default="Citizen")
    
    def save(self, *args, **kwargs):
        
        # if self.pk:  # Check if updating an existing citizen
        #     old_instance = Citizen.objects.filter(pk=self.pk).first()
        # if old_instance and old_instance.citizen_profile_picture:
        #     old_path = old_instance.citizen_profile_picture.path
        #     if os.path.exists(old_path):  # Delete old file
        #         default_storage.delete(old_path)
        
        # Hash the password before saving
        if not self.user_password.startswith('pbkdf2_sha256$'):
            self.user_password = make_password(self.user_password)
            
        super().save(*args, **kwargs)

    def verify_password(self, password):
        return check_password(password, self.user_password)
    
    def __str__(self):
        return f"{self.user_name}-{self.user_email}"

class Investigator(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=200)
    user_address = models.CharField(max_length=400)
    user_email = models.EmailField()
    user_phone_number = models.IntegerField()
    user_type=models.CharField(max_length=15,default="Investigator")
    def __str__(self):
        return f"{self.user_name}-{self.user_email}"

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.user_password.startswith('pbkdf2_sha256$'):
            self.user_password = make_password(self.user_password)
        super().save(*args, **kwargs)

    def verify_password(self, password):
        return check_password(password, self.user_password)