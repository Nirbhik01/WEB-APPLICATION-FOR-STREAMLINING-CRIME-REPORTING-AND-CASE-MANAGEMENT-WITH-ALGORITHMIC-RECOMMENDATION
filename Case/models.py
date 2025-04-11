from django.db import models
from userauths.models import Citizen as Ct
from userauths.models import Investigator as It

case_status_choices=[("FIR_Registration","FIR Registration"),("FIR_Verification","FIR Verification"),
                     ("Investigator_Assigning","Investigator Assigning"),("Investigation_Ongoing","Investigation Ongoing"),
                     ("Investigation_Termination","Investigation Termination")]

class Case(models.Model):
    #
    # contains only surface level details
    # like FIR number, reporter, investigator, status, upload date
    # and solved date
    
    
    case_id = models.AutoField(primary_key=True) # FIR number
    case_title= models.CharField(max_length=100) # FIR title
    reporter = models.ForeignKey(Ct,on_delete=models.DO_NOTHING, null=True)  
    investigator = models.ForeignKey(It, on_delete=models.DO_NOTHING,null=True)
    status = models.CharField(max_length=40, choices=case_status_choices, default="FIR_Registration")
    upload_date = models.DateTimeField(auto_now_add=True)
    solved_date= models.DateTimeField(null=True, blank=True,default=None) # exists if case is solved
    is_reporter_the_victim = models.BooleanField(choices=[("True","Yes"),("False","No")]) # true if reporter is victim
    crime_date= models.DateTimeField(null=True, blank=True) # date of crime
    crime_location= models.CharField(max_length=100, null=True, blank=True) # location of crime
    crime_description= models.TextField(null=True, blank=True) # description of crime
    crime_time= models.TimeField(null=True, blank=True) # time of crime
    
    
    def __str__(self):
        return f"Case {self.case_id} - {self.case_title} - {self.status} - {self.upload_date}"

class activity_log(models.Model):
    # contains logs of all activities performed on the case
    # like FIR registration, investigator assigning, etc.
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    activity = models.TextField(max_length=500) # description of activity
    activity_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Activity Log for {self.case.case_id} - {self.activity} - {self.activity_date}"
    
class evidence(models.Model):
    # contains evidence related to the case
    # like images, videos, documents, etc.
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    evidence_type = models.CharField(max_length=100) # type of evidence (image, video, document, etc.)
    if evidence_type == "image":
        evidence_file = models.ImageField(upload_to='media/evidence/') # file path of evidence
    elif evidence_type == "video":
        evidence_file = models.FileField(upload_to='media/evidence/') # file path of evidence
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Evidence for {self.case.case_id} - {self.evidence_type} - {self.upload_date}"