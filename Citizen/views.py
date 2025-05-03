from django.shortcuts import render
from userauths.models import Citizen as Ct
from userauths.models import Citizenship_photo as Cp
from Case.models import Case, Evidence
# import messages
from django.contrib import messages
from django.http import JsonResponse
# for recent image upload of report crime form 
import base64
from django.core.files.base import ContentFile
import os
from datetime import date, timedelta

def is_image_or_video(file_name):
    image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    video_exts = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm']
    audio_exts = ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a', '.wma', '.alac', '.aiff', '.amr']

    ext = os.path.splitext(file_name)[1].lower()
    
    if ext in image_exts:
        return 'image'
    elif ext in video_exts:
        return 'video'
    elif ext in audio_exts:
        return 'audio'
    else:
        return 'unknown'

def register_case(request):
    if request.method == 'POST':
        crime_type= request.POST.get('crime_type')
        crime_date= request.POST.get('crime_date')
        crime_time= request.POST.get('crime_time')
        crime_location= request.POST.get('crime_location')
        crime_location_link= request.POST.get('crime_location_link')
        crime_evidence = request.FILES.getlist ('crime_evidence')
        crime_description= request.POST.get('crime_description')
        citizenship = request.FILES.getlist ('citizenship')
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
        case.status = "FIR_Verification"
        case.save()
        # check evidence type and create evidence instance accordingly
        save_evidence(crime_evidence,case)

        user_photo = Ct.objects.get(user_id=user_id)

        if (not user_photo.user_recent_photo):
            user_photo.user_recent_photo = image_file
            user_photo.save() 
        elif (user_photo.user_recent_photo) :
            user_photo.user_recent_photo.delete()
            user_photo.user_recent_photo = image_file
            user_photo.recent_photo_upload_date = date.today()
            user_photo.save()

        for file in citizenship:
            # create an project and save
            citizenship_photo = Cp(user=user, citizenship_photo=file)
            citizenship_photo.save()

        messages.success(request, "Case registered successfully.")
        return JsonResponse({"status": "success", "message": "Case registered successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request."})

def save_evidence(crime_evidence,case):        
    for file in crime_evidence:
        # print("entered in evidence")
        file_type = is_image_or_video(file.name)
        if file_type == 'image':
            # print("entered in image")
            evidence = Evidence(case = case,
                            evidence_type = file_type,
                            evidence_pic_file = file,
                            )
            # print("evidence created")
            evidence.save()
        elif file_type == 'video':
            # print("entered in video")
            evidence = Evidence(case = case,
                            evidence_type = file_type,
                            evidence_vid_file = file,
                            )
            # print("evidence created")
            evidence.save()
        elif file_type == 'audio':
            # print("entered in audio")
            evidence = Evidence(case = case,
                            evidence_type = file_type,
                            evidence_audio_file = file,
                            )
            # print("evidence created")
            evidence.save()
        else:
            pass 
        
# Create your views here.
