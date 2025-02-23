from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.text import slugify
from django.core.files.storage import default_storage
import os

def citizen_profile_pic_path(instance, filename): #instance represents the current class object being used
    ext = filename.split('.')[-1]  # Get file extension (png, jpg, etc.)
    email_slug = slugify(instance.citizen_email.split('.')[0])  # Sanitize email
    new_filename = f"{email_slug}.{ext}"  # Create new filename
    return os.path.join('ReportEaseApp/ProfilePics/', new_filename)

class Citizen(models.Model):
    citizen_id = models.BigAutoField(primary_key=True)
    citizen_name = models.CharField(max_length=200)
    citizen_password = models.CharField(max_length=200)
    citizen_address = models.CharField(max_length=400)
    citizen_email = models.EmailField()
    citizen_phone_number = models.IntegerField()
    citizen_profile_picture = models.ImageField(upload_to = citizen_profile_pic_path,null=True, blank=True)
    
    def save(self, *args, **kwargs):
        
        # if self.pk:  # Check if updating an existing citizen
        #     old_instance = Citizen.objects.filter(pk=self.pk).first()
        # if old_instance and old_instance.citizen_profile_picture:
        #     old_path = old_instance.citizen_profile_picture.path
        #     if os.path.exists(old_path):  # Delete old file
        #         default_storage.delete(old_path)
        
        # Hash the password before saving
        if not self.citizen_password.startswith('pbkdf2_sha256$'):
            self.citizen_password = make_password(self.citizen_password)
            
        super().save(*args, **kwargs)

    def verify_password(self, password):
        return check_password(password, self.citizen_password)
    
    def __str__(self):
        return f"{self.citizen_name}-{self.citizen_email}"

class Investigator(models.Model):
    investigator_id = models.BigAutoField(primary_key=True)
    investigator_name = models.CharField(max_length=200)
    investigator_password = models.CharField(max_length=200)
    investigator_address = models.CharField(max_length=400)
    investigator_email = models.EmailField()
    investigator_phone_number = models.IntegerField()
    def __str__(self):
        return f"{self.investigator_name}-{self.investigator_email}"

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.investigator_password.startswith('pbkdf2_sha256$'):
            self.investigator_password = make_password(self.investigator_password)
        super().save(*args, **kwargs)

    def verify_password(self, password):
        return check_password(password, self.investigator_password)