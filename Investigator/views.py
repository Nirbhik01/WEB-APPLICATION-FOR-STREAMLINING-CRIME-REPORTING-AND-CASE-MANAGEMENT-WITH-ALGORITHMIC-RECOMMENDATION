from django.shortcuts import render,redirect
# import messages
from django.contrib import messages
from django.http import JsonResponse
from Case.models import Wanted as Wt
from Case.models import Case, Evidence
from userauths.models import Investigator as Iv,Citizenship_photo as Cp
import nltk
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

from ReportEaseApp.keyword_extraction import get_keywords

# Create your views here.
def UploadWanted(request):
    
    if request.method == 'POST':
        name = request.POST.get('Wanted_name')
        wanted_for = request.POST.get('Wanted_for')
        wanted_pic = request.FILES['Wanted_photo'] 
        
        # Create a new Wanted object and save it to the database
         
        wanted_post = Wt(
            wanted_name = name,
            wanted_reason = wanted_for,
            wanted_pic = wanted_pic
        )
        wanted_post.save()
        # messages.success(request, 'Wanted Post Created Successfully!')
        messages.success(request, 'Wanted Post Created Successfully!')
        # return JsonResponse({"status": "success", "message": "Wanted Post Created."})
        return redirect("ReportEaseApp:HomePage")
    # Change 'success_page' to your desired URL or view name
    
    return JsonResponse({"status":"error","message":"An error occured"})  # Render the upload form template

def mark_case_registered(request,id):
    try:
        case = Case.objects.get(case_id=id)
        case.is_registered = True
        user=None 
        if request.session.get('user_type') == 'Investigator':
            user = Iv.objects.get(user_id=request.session.get('user_id'))
        case.status = "Investigator_Assigning"
        case.registered_by = user
        case.save()
        
        citizen = case.reporter
        
        subject = "Case Registered"
        html_message = f"""
        <html>
        <body>
            <h2 style="color:#2C3E50;">Hello {citizen.user_name},</h2>
            <p>Your case titled <b>{case.case_title}</b> has been <strong>registered</strong> and marked as registered for further investigation.</p>
        </body>
        </html>
        """
        send_case_notification_email(citizen.user_email, citizen.user_name, subject, html_message)
        print("mail registered sending to ", citizen.user_email)
        
        def keyword_extraction_bg():
            print("extracting keyword")
            try:
                # nltk.data.find('corpora/wordnet')
                # nltk.data.find('tokenizers/punkt')
                # nltk.data.find('taggers/averaged_perceptron_tagger_eng')
                result = get_keywords(case.crime_description)
                print(f"Extracted keywords for case {case.case_id}: {result}")
                # Optionally: Save to DB or attach to case
                keyword_list = list(result.keys())
                keywords_str = ",".join(keyword_list)
                case.keywords = keywords_str
                case.save()
            except Exception as e:
                print(f"Keyword extraction failed: {e}")
            print("matching cases and investigators")
        threading.Thread(target=keyword_extraction_bg).start()
        
        messages.success(request,"Case marked as Registered")
        return JsonResponse({"status": "success"})
    except Case.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Case not found."})
    
def mark_case_not_registered(request,id):
    try:
        # delete case from db
        case = Case.objects.get(case_id=id)
        citizen = case.reporter
        # also delete all its associated files from their respective paths
        evidences = Evidence.objects.filter(case=case)
        for evidence in evidences:
            if evidence.evidence_pic_file:
                evidence.evidence_pic_file.delete()
                evidence.delete()
            if evidence.evidence_vid_file:
                evidence.evidence_vid_file.delete()
                evidence.delete()
            
        citizen = case.reporter
        citizen.user_recent_photo.delete()
        citizen.recent_photo_upload_date.delete()
        citizen.save()
        citizenship_photos = Cp.objects.filter(user=citizen)
        for photo in citizenship_photos:
            photo.citizenship_photo.delete()
            photo.delete()
        subject = "Case Not Registered"
        html_message = f"""
        <html>
        <body>
            <h2 style="color:#2C3E50;">Hello {citizen.user_name},</h2>
            <p>We're sorry to inform you that your case titled <b>{case.case_title}</b> was not accepted after review.</p>
        </body>
        </html>
        """
        send_case_notification_email(citizen.user_email, citizen.user_name, subject, html_message)        
        case.delete()
        print("mail not registered sending to ", citizen.user_email)
        messages.success(request,"Case Removed Successfully")
        return JsonResponse({"status": "success"})
    
    except:
        return JsonResponse({"status": "error", "message": "Operation Failed"})
    
def send_case_notification_email(to_email, user_name, subject, html_message):
    def send():
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(f"{settings.MAIL_ID}", f"{settings.MAIL_PWD}")

            msg = MIMEMultipart("alternative")
            msg['From'] = f"{settings.MAIL_ID}"
            msg['To'] = to_email
            msg['Subject'] = subject

            # Optional plain version
            text = "This email requires an HTML-capable viewer."
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html_message, "html")

            msg.attach(part1)
            msg.attach(part2)

            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()
        except Exception as e:
            print("Email sending failed:", str(e))

    threading.Thread(target=send).start() 
    

# def extract_case_keywords(case_id):
#     try:
#         case = Case.objects.get(case_id=case_id)
#         keywords = get_keywords(case.case_description)  # or any relevant field
#         # Optionally, store the keywords in the database if needed:
#         case.keywords = keywords  # if you have a `keywords` JSONField or TextField
#         case.save()
#         return {"status": "success", "keywords": keywords}
#     except Case.DoesNotExist:
#         return {"status": "error", "message": "Case not found."}
# Create your views here.