from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.text import slugify
from django.core.files.storage import default_storage
import os,datetime

def citizen_profile_pic_path(instance, filename): #instance represents the current class object being used
    ext = filename.split('.')[-1]  # Get file extension (png, jpg, etc.)
    email_slug = slugify(instance.user_email.split('.')[0])  # Sanitize email
    new_filename = f"{email_slug}.{ext}"  # Create new filename
    return os.path.join('ReportEaseApp/ProfilePics/Citizen', new_filename)

def citizen_citizenship_pic_path(instance, filename): #instance represents the current class object being used
    ext = filename.split('.')[-1]  # Get file extension (png, jpg, etc.)
    email_slug = slugify(instance.user.user_email.split('.')[0])  # Sanitize email
    length = Citizenship_photo.objects.filter(user=instance.user).count()
    new_filename = f"{email_slug}-{length+1}.{ext}"  # Create new filename
    return os.path.join('ReportEaseApp/Documents', new_filename)

def citizen_recent_pic_path(instance, filename): #instance represents the current class object being used
    ext = filename.split('.')[-1]  # Get file extension (png, jpg, etc.)
    email_slug = slugify(instance.user_email.split('.')[0])  # Sanitize email
    new_filename = f"{email_slug}.{ext}"  # Create new filename
    return os.path.join('ReportEaseApp/Recent_Photo', new_filename)


class Citizen(models.Model):
    user_id = models.BigAutoField(primary_key = True)
    user_name = models.CharField(max_length = 200)
    user_password = models.CharField(max_length = 200)
    user_address = models.CharField(max_length = 400)
    user_email = models.EmailField()
    user_phone_number = models.IntegerField()
    user_profile_picture = models.ImageField(upload_to = citizen_profile_pic_path, null = True, blank = True)
    user_type=models.CharField(max_length = 15, default="Citizen")
    user_recent_photo = models.ImageField(upload_to = citizen_recent_pic_path,null = True, blank = True)
    recent_photo_upload_date = models.DateField(default = None, null = True, blank = True)
    # auto now add is set only during creation of the object 
    joined_on = models.DateField(auto_now_add=True)
    # auto now sets everytime an object is saved
    updated_on = models.DateTimeField(auto_now=True)

    
    def save(self, *args, **kwargs):
        if not self.user_password.startswith('pbkdf2_sha256$'):
            self.user_password = make_password(self.user_password)
            
        super().save(*args, **kwargs)

    def verify_password(self, password):
        return check_password(password, self.user_password)
    
    def __str__(self):
        return f"{self.user_name}-{self.user_email}"

class Citizenship_photo(models.Model):
    user = models.ForeignKey(Citizen, on_delete=models.SET_NULL,null=True)
    citizenship_photo = models.ImageField(upload_to=citizen_citizenship_pic_path,null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.user_email}-{self.citizenship_photo}"


def Investigator_profile_pic_path(instance, filename): #instance represents the current class object being used
    ext = filename.split('.')[-1]  # Get file extension (png, jpg, etc.)
    email_slug = slugify(instance.user_email.split('.')[0])  # Sanitize email
    new_filename = f"{email_slug}.{ext}"  # Create new filename
    return os.path.join('ReportEaseApp/ProfilePics/Investigator', new_filename)

class Investigator(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=200)
    user_address = models.CharField(max_length=400)
    user_email = models.EmailField()
    user_phone_number = models.IntegerField()
    user_type=models.CharField(max_length=15,default="Investigator")
    user_profile_picture = models.ImageField(upload_to = Investigator_profile_pic_path,null=True, blank=True)
    user_district=models.CharField(max_length=200,default=None)
    joined_on = models.DateField(auto_now_add=True)
    keywords = models.TextField(default=None,blank=True,null=True)
    
    def __str__(self):
        return f"{self.user_name}-{self.user_email}"

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.user_password.startswith('pbkdf2_sha256$'):
            self.user_password = make_password(self.user_password)
        super().save(*args, **kwargs)

    def verify_password(self, password):
        return check_password(password, self.user_password)
    
    