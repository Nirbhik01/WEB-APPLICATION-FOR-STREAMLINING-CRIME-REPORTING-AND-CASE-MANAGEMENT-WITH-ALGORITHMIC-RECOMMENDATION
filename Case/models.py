from django.db import models
from userauths.models import Citizen as Ct
from userauths.models import Investigator as It
import os
from django.utils.text import slugify

def Wanted_pic_path(instance, filename): #instance represents the current class object being used
    ext = filename.split('.')[-1]  # Get file extension (png, jpg, etc.)
    email_slug = slugify(instance.wanted_name.split('.')[0])  # Sanitize email
    new_filename = f"{email_slug}.{ext}"  # Create new filename
    return os.path.join('ReportEaseApp/Wanted_Pics', new_filename)

case_status_choices=[("FIR_Registration","FIR Registration"),("FIR_Verification","FIR Verification"),
                     ("Investigator_Assigning","Investigator Assigning"),("Investigation_Ongoing","Investigation Ongoing"),
                     ("Investigation_Termination","Investigation Termination")]

CRIME_CATEGORIES = [
    ('ANTI_SOCIAL', 'Antisocial Behaviour'),
    ('BURGLARY', 'Burglary'),
    ('CRIMINAL_DAMAGE', 'Criminal Damage'),
    ('CYBER_CRIME', 'CyberCrime'),
    ('FRAUD', 'Fraud'),
    ('HATE_CRIME', 'Hate Crime'),
    ('ROBBERY', 'Robbery'),
    ('RURAL_CRIME', 'Rural Crime'),
    ('SPIKING', 'Spiking'),
    ('STACKING', 'Stacking'),
]


class Case(models.Model):
    #
    # contains only surface level details
    # like FIR number, reporter, investigator, status, upload date
    # and solved date
    
    
    case_id = models.AutoField(primary_key=True) # FIR number
    case_title= models.CharField(max_length=100,choices=CRIME_CATEGORIES) # FIR title
    reporter = models.ForeignKey(Ct,on_delete=models.DO_NOTHING, null=True)  
    investigator = models.ForeignKey(It, on_delete=models.DO_NOTHING,null=True,blank=True)
    status = models.CharField(max_length=40, choices=case_status_choices, default="FIR_Registration")
    upload_date = models.DateTimeField(auto_now_add=True)
    solved_date= models.DateTimeField(null=True, blank=True,default=None) # exists if case is solved
    is_reporter_the_victim = models.BooleanField(choices=[(True,"Yes"),(False,"No")]) # true if reporter is victim
    crime_date= models.DateField(null=True, blank=True) # date of crime
    crime_location= models.CharField(max_length=100, null=True, blank=True) # location of crime
    crime_description= models.TextField(null=True, blank=True) # description of crime
    crime_time= models.TimeField(null=True, blank=True) # time of crime
    crime_link = models.CharField(null=True, blank=True,max_length=1000) #google map link of crime location
    is_registered = models.BooleanField(default=False) # true if FIR is registered
    
    def __str__(self):
        return f"Case {self.case_id} - {self.case_title} - {self.status} - {self.upload_date}"

class Activity_log(models.Model):
    # contains logs of all activities performed on the case
    # like FIR registration, investigator assigning, etc.
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    activity = models.TextField(max_length=500) # description of activity
    activity_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Activity Log for {self.case.case_id} - {self.activity} - {self.activity_date}"


def Evidence_pic_path(instance, filename): #instance represents the current class object being used
    ext = filename.split('.')[-1]  # Get file extension (png, jpg, etc.)
    id_slug = slugify(instance.case.case_id)  # Sanitize email
    length = Evidence.objects.filter(case=instance.case).count()
    new_filename = f"{id_slug}-{length+1}.{ext}"   # Create new filename
    return os.path.join('ReportEaseApp/Evidence/Photo', new_filename)

def Evidence_vid_path(instance, filename): #instance represents the current class object being used
    ext = filename.split('.')[-1]  # Get file extension (png, jpg, etc.)
    id_slug = slugify(instance.case.case_id)  # Sanitize email
    # check for the number of files that exist with the case
    length = Evidence.objects.filter(case=instance.case).count()
    new_filename = f"{id_slug}-{length+1}.{ext}"  # Create new filename
    return os.path.join('ReportEaseApp/Evidence/Video', new_filename)
    
class Evidence(models.Model):
    # contains evidence related to the case
    # like images, videos, documents, etc.
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    evidence_type = models.CharField(max_length=100) # type of evidence (image, video, document, etc.)
    evidence_pic_file = models.ImageField(upload_to= Evidence_pic_path, default=None) # file path of evidence
    evidence_vid_file = models.FileField(upload_to= Evidence_vid_path, default=None) # file path of evidence
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Evidence for {self.case.case_id} - {self.evidence_type} - {self.upload_date}"
    
    
class Wanted(models.Model):
    wanted_id = models.AutoField(primary_key=True) # id of wanted person
    wanted_pic = models.ImageField(upload_to=Wanted_pic_path) # image of wanted person
    wanted_name = models.CharField(max_length=100) # name of wanted person
    wanted_reason= models.TextField() # reason for being wanted
    upload_date=models.DateField(auto_now_add=True,null=False) # date of upload

    
    def __str__(self):
        return f" {self.wanted_id} - {self.wanted_name} - {self.wanted_reason}"