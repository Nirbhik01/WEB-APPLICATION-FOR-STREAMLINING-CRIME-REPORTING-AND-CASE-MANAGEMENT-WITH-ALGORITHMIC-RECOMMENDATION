from django.shortcuts import render

from django.http import JsonResponse
from .models import *
from userauths.models import Citizen as Ct

# for recent image upload of report crime form 
import base64
from django.core.files.base import ContentFile

import os

def is_image_or_video(file_name):
    image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    video_exts = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm']

    ext = os.path.splitext(file_name)[1].lower()
    
    if ext in image_exts:
        return 'image'
    elif ext in video_exts:
        return 'video'
    else:
        return 'unknown'


def get_wanted_list():
    # Fetch the list of wanted individuals from the database and 
    wanted_list = Wanted.objects.all().values('wanted_name', 'wanted_reason', 'wanted_pic','upload_date')
    # sort wanted list by upload_date so that recent date comes first
    wanted_list = wanted_list.order_by('-upload_date')
    
    # Convert the queryset to a list of dictionaries
    wanted_list = list(wanted_list)
    
    return list(wanted_list)

def register_case(request):
    crime_type= request.POST.get('crime_type')
    crime_date= request.POST.get('crime_date')
    crime_time= request.POST.get('crime_time')
    crime_location= request.POST.get('crime_location')
    crime_location_link= request.POST.get('crime_location_link')
    crime_evidence= request.FILES['crime_evidence']
    crime_description= request.POST.get('crime_description')
    citizenship = request.FILES['citizenship']
    yes_no= True if request.POST.get('yes_no') else False
    # recent_photo = request.FILES.get('recent_photo')
    image_data_url = request.POST.get('recent_photo_dataurl')
    image_file=None
    if image_data_url:
        format, imgstr = image_data_url.split(';base64,') 
        ext = format.split('/')[-1]
        image_file = ContentFile(base64.b64decode(imgstr), name=f"recent_photo.{ext}")
    
    
    
    # Get the user id from the session
    user_id = request.session.get('user_id')
    user = Ct.objects.get(user_id=user_id)
    
    # Create a new case instance
    case = Case(
        case_title=crime_type,
        reporter=user,
        is_reporter_the_victim=yes_no,
        crime_date=crime_date,
        crime_location=crime_location,
        crime_description=crime_description,
        crime_time=crime_time,
        crime_link=crime_location_link
    )
    case.save()
    # check evidence type and create evidence instance accordingly
    file_type = is_image_or_video(crime_evidence.name)

    if file_type == 'image':
        evidence = Evidence(case = case,
                        evidence_type = file_type,
                        evidence_pic_file = crime_evidence,
                        )
        evidence.save()
    elif file_type == 'video':
        evidence = Evidence(case = case,
                        evidence_type = file_type,
                        evidence_vid_file = crime_evidence,
                        )
        evidence.save()
    else:
        pass 
    
    user_photo = Ct.objects.get(user_id=user_id)
    user_photo.user_recent_photo = image_file
    user_photo.user_citizenship = citizenship
    user_photo.save()
    
    return True
    
    
    
# Create your views here.
