from django.shortcuts import render,redirect
# import reverse
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from Case.models import Case,Evidence,Wanted,Activity_log
from userauths.models import Citizen as Ct, Citizenship_photo as Cp, Investigator as Iv
from chat.models import Message
from django.db.models import Count,Q
from datetime import datetime, timedelta

from django.conf import settings

from django.http import HttpResponse, Http404
from ReportEase.encryption import decrypt_file

from Investigator.views import send_case_notification_email
from .models import Notification
# from Case.views import display_cases_for_homepage
from Citizen.views import save_evidence

from django.conf import settings

def LandingPage(request):
    
    return render(request, 'LandingPage.html' )

# enable get_news(request) during presentation
def HomePage(request):
    login_check = check_for_login(request)
    if login_check:
        return login_check
    wanted_data = get_wanted_list()
    
    return render(request, 'HomePage.html',{'wanted_list': wanted_data,
                                            # uncomment for presentation
                                            # 'news_articles':get_news(request),
                                            })

def UploadWantedPage(request):
    login_check = check_for_login(request)
    if login_check:
        return login_check
    return render(request, 'UploadWantedPage.html')

def ReviewFirPage(request,id):
    login_check = check_for_login(request)
    if login_check:
        return login_check
    return render(request, 'ReviewFirPage.html')

def CaseListPage(request):
    login_check = check_for_login(request)
    if login_check:
        return login_check
    return render(request, 'CaseListPage.html')

def CasePage(request,id):
    login_check = check_for_login(request)
    if login_check:
        return login_check
    return render(request, 'CasePage.html')

def ReportCrimePage(request):
    login_check = check_for_login(request)
    if login_check:
        return login_check
    return render(request, 'ReportCrimePage.html')

def ProfilePage(request):
    login_check = check_for_login(request)
    if login_check:
        return login_check
    return render(request, 'ProfilePage.html')

def EditProfilePage(request):
    return render(request,'EditProfilePage.html')

def check_for_login(request):
    try:

        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')
        if not(user_id and user_type):
            messages.warning(request,"You must be logged in to view that page")
            return redirect('userauths:LoginPage')
    except:
        
        messages.warning(request,"You must be logged in to view that page")
        return redirect('userauths:LoginPage')
        
def case_details(request,id):
    try:
        user_type = request.session.get('user_type')
        data = dict()
        case = Case.objects.get(case_id=id)
        case_data = None
        if user_type == 'Investigator':
            case_data = {
                'case_id': case.case_id,
                'case_title': case.case_title,
                'reporter': str(case.reporter.user_name), 
                "reporter_pic":str(case.reporter.user_profile_picture.url),# convert ForeignKey to string or ID
                'upload_date': case.upload_date,
                'is_reporter_the_victim': case.is_reporter_the_victim,
                'crime_date': case.crime_date,
                'crime_location': case.crime_location,
                'crime_description': case.crime_description,
                'crime_time': case.crime_time,
                'crime_link': case.crime_link,
            }
            
        elif user_type == 'Citizen':
            case_data = {
                'case_id': case.case_id,
                'case_title': case.case_title,
                # 'investigator': str(case.investigator.user_name), 
                # "investigator_pic":str(case.investigator.user_profile_picture.url),# convert ForeignKey to string or ID
                'upload_date': case.upload_date,
                # 'is_reporter_the_victim': case.is_reporter_the_victim,
                'crime_date': case.crime_date,
                'crime_location': case.crime_location,
                'crime_description': case.crime_description,
                'crime_time': case.crime_time,
                'crime_link': case.crime_link,
            }
            if case.investigator:
                case_data['investigator'] = str(case.investigator.user_name)
                case_data["investigator_pic"] = str(case.investigator.user_profile_picture.url)
                case_data["investigator_email"] = str(case.investigator.user_email)
           
        elif user_type == 'Admin':
            # get all investigators who are involved in 4 cases or less
            available_investigators = Iv.objects.annotate(
                active_case_count=Count('case', filter=~Q(case__status="Investigation_Termination"))
            ).filter(active_case_count__lt=4)

            available_investigators_data = list(
                available_investigators.values('user_id', 'user_name', 'user_email')
            )

            data['available_investigators'] = available_investigators_data
            # print(data['available_investigators'])
                        
            case_data = {
                'case_id': case.case_id,
                'case_title': case.case_title,
                'reporter': str(case.reporter.user_name), 
                "reporter_pic":str(case.reporter.user_profile_picture.url),# convert ForeignKey to string or ID
                'upload_date': case.upload_date,
                'is_reporter_the_victim': case.is_reporter_the_victim,
                'crime_date': case.crime_date,
                'crime_location': case.crime_location,
                'crime_description': case.crime_description,
                'crime_time': case.crime_time,
                'crime_link': case.crime_link,
                "registered_by":str(case.registered_by.user_name), #
                "registered_by_pic":str(case.registered_by.user_profile_picture.url), #
                "available_investigators":available_investigators_data, #
                "best_investigator_name":str(case.best_investigator.user_name), #
                "best_investigator_email":str(case.best_investigator.user_email), #  
            }
        data['case_data']=(case_data)
        
        evidences = Evidence.objects.filter(case=case)
        evidence_Data=dict()
            
        for evidence in evidences:
        #    append into the evidence_Date dictionary
            evidence_Data[evidence.id] = {
                'evidence_id': evidence.id,
                'evidence_type': evidence.evidence_type,
                'evidence_pic_file': request.build_absolute_uri(reverse("ReportEaseApp:serve_decrypted_evidence", args=[evidence.id, 'pic'])) if evidence.evidence_pic_file else None,
                'evidence_vid_file': request.build_absolute_uri(reverse("ReportEaseApp:serve_decrypted_evidence", args=[evidence.id, 'vid'])) if evidence.evidence_vid_file else None,
                # 'evidence_vid_file': str(evidence.evidence_vid_file.url) if evidence.evidence_vid_file else None, 
            }
            
        data['evidence'] = evidence_Data
        
        citizenship = Cp.objects.filter(user=case.reporter)
        citizenship_Data = dict()
        for citizen in citizenship:
            citizenship_Data[citizen.id] = {
                'citizenship_id': citizen.id,
                'citizenship_photo': request.build_absolute_uri(
                                            reverse("ReportEaseApp:serve_decrypted_citizenship_photo", args=[citizen.id])
                                        ) if citizen.citizenship_photo else None,
            }

        data['citizenship'] = citizenship_Data
        
        data['recent_photo'] = {
            'recent_photo': request.build_absolute_uri(
                                reverse("ReportEaseApp:serve_decrypted_recent_photo", args=[case.reporter.user_id])
                            ) if case.reporter.user_recent_photo else None
        }
 
        return JsonResponse(data, safe=False)
    
    except Case.DoesNotExist:
        return JsonResponse({"error": "Case not found"}, status=404)

def case_status(request,id):
    try:
        case = Case.objects.get(case_id=id)
        if case.status=="Investigation_Termination" and case.was_successful:
            return JsonResponse({"status":"solved"})
        elif case.status=="Investigation_Termination" and (not case.was_successful):
            return JsonResponse({"status":"terminated_but_unsolved"})
        else:
            return JsonResponse({"status" : str(case.status)})
        
        
    except Case.DoesNotExist:
        return JsonResponse({"error" : "An error Occured"})
    
def get_wanted_list():
    # Fetch the list of wanted individuals from the database 
    wanted_list = Wanted.objects.all().values('wanted_name', 'wanted_reason', 'wanted_pic','upload_date')
    # sort wanted list by upload_date so that recent date comes first
    wanted_list = wanted_list.order_by('-upload_date')
    
    # Convert the queryset to a list of dictionaries
    wanted_list = list(wanted_list)
    
    return (wanted_list)

def activity_log(request,id):
    if request.method =="POST":
        activity_name = request.POST.get("activity_name")
        activity_description = request.POST.get("activity_description")
        activity_file = request.FILES.getlist("activity_file")
        
        user = None
        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')
        if user_type == 'Citizen':
            user = Ct.objects.get(user_id=user_id)
        elif user_type=="Investigator":
            user = Iv.objects.get(user_id=user_id)
        
        case = Case.objects.get(case_id = id)
        
        print(f"activity log - {case,activity_name,activity_description,activity_file}")
        if user_type == 'Citizen':
            activity_log = Activity_log(case=case,activity_title=activity_name,activity_description=activity_description,uploaded_by_citizen=user)
            activity_log.save()
            investigator = case.investigator
            subject_investigator = "Case Update"
            html_message_investigator = f"""
            <html>
            <body>
                <p>Activity log of case <b>{case.case_title} </b> has been updated by {case.reporter.user_name}.</p>
            </body>
            </html>
            """
            send_case_notification_email(investigator.user_email, investigator.user_name, subject_investigator, html_message_investigator)
            
        elif user_type == 'Investigator':
            activity_log = Activity_log(case=case,activity_title=activity_name,activity_description=activity_description,uploaded_by_investigator=user)
            activity_log.save()
            citizen = case.reporter
            subject = "Case update"
            html_message = f"""
            <html>
            <body>
                <p>Activity log of case <b>{case.case_title} </b> has been updated by {case.investigator.user_name}.</p>
            </body>
            </html>
            """
            send_case_notification_email(citizen.user_email, citizen.user_name, subject, html_message)
        
        if activity_file:
            save_evidence(activity_file,case) # Imported from Citizen.Views
            
        return JsonResponse({"status":"success"})
        # print(activity_name,activity_description,activity_file)
 
def fetch_activity_log(request,id):
    case = Case.objects.get(case_id = id)
    activity_log = Activity_log.objects.filter(case=case).values('activity_title','activity_description','activity_date',"uploaded_by_citizen__user_name","uploaded_by_investigator__user_name").order_by('-activity_date')
    activity_log = list(activity_log)      
    return JsonResponse(activity_log, safe=False)
    
def fetch_user_details(request):
    user_id = request.session.get("user_id")
    user_type = request.session.get("user_type")
    user = None
    if user_type == 'Citizen':
        user = Ct.objects.filter(user_id=user_id).values('user_name','user_email','user_phone_number', 'user_password','user_address','user_profile_picture')
    elif user_type == 'Investigator':
        user = Iv.objects.filter(user_id=user_id).values('user_name','user_email','user_phone_number', 'user_password','user_address','user_profile_picture')
    return JsonResponse(list(user),safe=False)

def fetch_terminated_case_details(request):
    logged_in_user_type = request.session.get("user_type")
    user_id = request.session.get("user_id")
    case = None
    try:
        if logged_in_user_type == 'Citizen':
            user = Ct.objects.get(user_id=user_id)
            case = Case.objects.filter(reporter = user,status='Investigation_Termination').values("case_id","case_title","investigator__user_name")
            
        elif logged_in_user_type == 'Investigator':
            user = Iv.objects.get(user_id=user_id)
            case = Case.objects.filter(investigator = user,status='Investigation_Termination').values("case_id","case_title","reporter__user_name")
        
        return JsonResponse(list(case),safe=False)
    except:
        return JsonResponse({"status":"error"})

def save_edited_user_details(request):
    if request.method == "POST":
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        email = request.POST.get('email', '')
        number = request.POST.get('number', '')
        address = request.POST.get('address', '')
        password = request.POST.get('password', '')
        profile_pic = request.FILES.getlist('profile_pic')

        user_id = request.session.get("user_id")
        user_type = request.session.get("user_type")
        user = None
        if user_type == 'Citizen':
            user = Ct.objects.get(user_id=user_id)
        elif user_type == 'Investigator':
            user = Iv.objects.get(user_id=user_id)
        
        # Update basic user fields
        user.user_name = fname+" "+lname 
        user.user_email = email
        if password:
            user.user_password=password
        user.user_phone_number = number
        user.user_address = address
        if profile_pic:
            #delete current profile pic from the db and also the device
            if user.user_profile_picture and user.user_profile_picture.name:
                user.user_profile_picture.delete(save=False)
            user.user_profile_picture = profile_pic[0]
        user.save()
        messages.success(request, "Profile Updated successfully.")
        # Update additional details
        return JsonResponse({"status": "success", "message": "Profile updated successfully."})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)    
    
def assign_investigator(request,id):
    if request.method == 'POST':
        try:
            investigators_list = request.POST.get("investigators_list")
            investigator = Iv.objects.get(user_email=investigators_list)
            case = Case.objects.get(case_id=id)
            case.investigator = investigator
            case.status="Investigation_Ongoing"
            case.save()
            citizen = case.reporter
            subject = "Investigator Assigned"
            html_message = f"""
            <html>
            <body>
                <h2 style="color:#2C3E50;">Hello {citizen.user_name},</h2>
                <p>Investigator {case.investigator.user_name} has been assigned to your case.</p>
                <p><b>{case.case_title}</b></p>
            </body>
            </html>
            """
            send_case_notification_email(citizen.user_email, citizen.user_name, subject, html_message)
            # now send mail to the investigator
            investigator = case.investigator
            subject_investigator = "Case Assigned"
            html_message_investigator = f"""
            <html>
            <body>
                <h2 style="color:#2C3E50;">Hello {investigator.user_name},</h2>
                <p>Case <b>{case.case_title} - {case.reporter.user_name}</b> has been assigned to you.</p>
                
            </body>
            </html>
            """
            send_case_notification_email(investigator.user_email, investigator.user_name, subject_investigator, html_message_investigator)
            
            messages.success(request, "Investigator assigned successfully.")
            return JsonResponse({"status":"success"})
        except:
            return JsonResponse({"status":"error","message":"Error Assigning Investigator."})
    
    return JsonResponse({"status":"request","message":"Invalid request method."})
 
def mark_case_successfully_terminated(request,id):
    case = Case.objects.get(case_id=id)
    case.status="Investigation_Termination"

    # insert today's date time and decrease 5.75 hours
    case.terminated_date = datetime.now() - timedelta(hours=5, minutes=45)
    
    case.was_successful=True
    case.save()
    citizen = case.reporter
    subject = "Investigation Terminated"
    html_message = f"""
    <html>
    <body>
        <h2 style="color:#2C3E50;">Hello {citizen.user_name},</h2>
        <p>Your case titled <b>{case.case_title}</b> has been successfully terminated.</p>
    </body>
    </html>
    """
    send_case_notification_email(citizen.user_email, citizen.user_name, subject, html_message)
    return JsonResponse({"status":"success"}) 

def mark_case_unsuccessfully_terminated(request,id):
    case = Case.objects.get(case_id=id)
    case.status="Investigation_Termination"
    
    # insert today's date time and decrease 5.75 hours
    case.terminated_date = datetime.now() - timedelta(hours=5, minutes=45)
    
    case.was_successful=False
    case.save()
    citizen = case.reporter
    subject = "Investigation Terminated"
    html_message = f"""
    <html>
    <body>
        <h2 style="color:#2C3E50;">Hello {citizen.user_name},</h2>
        <p>Investigation on your case titled <b>{case.case_title}</b> was unsuccessfull and has been terminated.</p>
    </body>
    </html>
    """
    send_case_notification_email(citizen.user_email, citizen.user_name, subject, html_message)
    return JsonResponse({"status":"success"}) 

def get_news(request):
    from eventregistry import EventRegistry,QueryArticlesIter
    # allowUseOfArchive=False will allow us to search only over the last month of data
    er = EventRegistry(apiKey = settings.NEWS_AI_API_KEY, allowUseOfArchive=False)
    usUri = er.getLocationUri("USA") 
    # get the URIs for the companies and the category
    crimeUri = er.getCategoryUri("crime")

    q = QueryArticlesIter(
        categoryUri = crimeUri)

    simplified_articles = []
    seen_titles = set()

    # Limit to 8 simplified, unique articles
    for art in q.execQuery(er, sortBy="date", maxItems=30):  # fetch more in case of duplicates
        title = art.get('title')
        if title and title not in seen_titles:
            seen_titles.add(title)
            simplified_articles.append({
                'title': title,
                'link': art.get('url'),
                'description': art.get('body'),
                'image_url': art.get('image'),
                'source_name': art.get('source', {}).get('title'),
                'pubDate': art.get('dateTimePub').split("T")[0],
            })

        if len(simplified_articles) == 8:
            break

    return simplified_articles
     
def serve_decrypted_evidence(request, evidence_id, media_type):
    try:
        evidence = Evidence.objects.get(pk=evidence_id)
        file_field = getattr(evidence, f"evidence_{media_type}_file")
        if not file_field:
            raise Http404("File not found")

        decrypted_content = decrypt_file(file_field.path)

        content_type = {
            'pic': 'image/jpeg',
            'vid': 'video/mp4',
            'audio': 'audio/mpeg',
        }.get(media_type, 'application/octet-stream')

        return HttpResponse(decrypted_content, content_type=content_type)

    except Evidence.DoesNotExist:
        raise Http404("Evidence not found") 
    
def serve_decrypted_citizenship_photo(request, citizenship_id):
    try:
        
        photo = Cp.objects.get(pk=citizenship_id)
        file_field = photo.citizenship_photo
        if not file_field:
            raise Http404("Photo not found")

        decrypted_content = decrypt_file(file_field.path)
        return HttpResponse(decrypted_content, content_type='image/jpeg')

    except Cp.DoesNotExist:
        raise Http404("Photo not found")

def serve_decrypted_recent_photo(request, user_id):
    try:
        citizen = Ct.objects.get(user_id=user_id)
        file_field = citizen.user_recent_photo
        if not file_field:
            raise Http404("Photo not found")

        decrypted_content = decrypt_file(file_field.path)
        return HttpResponse(decrypted_content, content_type='image/jpeg')

    except Ct.DoesNotExist:
        raise Http404("User not found")

def get_chat_messages(request, case_id):
    try:
        case = Case.objects.get(case_id=case_id)
        messages = Message.objects.filter(case=case).order_by('timestamp')
        
        messages_data = []
        for msg in messages:
            message_data = {
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_read': msg.is_read,
                'sender_type': 'Citizen' if msg.sender_citizen else 'Investigator',
                'sender_name': msg.sender_citizen.user_name if msg.sender_citizen else msg.sender_investigator.user_name,
                'sender_id': msg.sender_citizen.user_id if msg.sender_citizen else msg.sender_investigator.user_id
            }
            messages_data.append(message_data)
            
        return JsonResponse({'messages': messages_data}, safe=False)
    except Case.DoesNotExist:
        return JsonResponse({"error": "Case not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def mark_messages_read(request, case_id):
    try:
        # user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')
        case = Case.objects.get(case_id=case_id)
        messages = None
        
        if user_type == 'Citizen':
            messages = Message.objects.filter(case=case, sender_investigator = case.investigator)
            for message in messages:
                message.is_read = True
                message.save()
        elif user_type == 'Investigator':
            messages = Message.objects.filter(case=case, sender_citizen = case.reporter)
            for message in messages:
                message.is_read = True
                message.save()    
        return JsonResponse({"status":"success"})
    except:
        return JsonResponse({"status":"error"})

def notification_view(request):
    user_type = request.session.get("user_type")
    user_id = request.session.get("user_id")

    notifications = []

    if user_type == "Citizen":
        user = Ct.objects.get(user_id=user_id)
        notifications_query = Notification.objects.filter(
            belongs_to_citizen=user
        ).order_by('-timestamp')
        for notification in notifications_query:
            notifications.append([notification.message,notification.timestamp])
        # Mark as read
        Notification.objects.filter(
            belongs_to_citizen=user,
            status="UNREAD"
        ).update(status="READ")
        
    elif user_type == "Investigator":
        user = Iv.objects.get(user_id=user_id)
        notifications_query = Notification.objects.filter(
            belongs_to_investigator=user
        ).order_by('-timestamp')
        for notification in notifications_query:
            notifications.append([notification.message,notification.timestamp])
        # Mark as read
        Notification.objects.filter(
            belongs_to_investigator=user,
            status="UNREAD"
        ).update(status="READ")
    print("notification-------------",notifications)
    return JsonResponse({"notifications":notifications})

def fetch_number_of_notifications(request):
    user_id = request.session.get("user_id")
    user_type = request.session.get("user_type")
    user = None
    if user_type == 'Citizen':
        user = Ct.objects.get(user_id=user_id)
        notifications = Notification.objects.filter(belongs_to_citizen=user,status="UNREAD").count()
        return JsonResponse({"notification_count":notifications})
    elif user_type == "Investigator":
        user = Ct.objects.get(user_id=user_id)
        notifications = Notification.objects.filter(belongs_to_investigator=user,status="UNREAD").count()
        return JsonResponse({"notification_count":notifications})
    return JsonResponse({"notification_count":0})