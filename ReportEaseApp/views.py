from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from Case.models import Case,Evidence,Wanted,Activity_log
from userauths.models import Citizen as Ct, Citizenship_photo as Cp
from Case.views import display_cases
from Citizen.views import save_evidence,is_image_or_video
# from userauths.views import get_current_user

def LandingPage(request):
    return render(request, 'LandingPage.html')

def HomePage(request):
    login_check = check_for_login(request)
    if login_check:
        return login_check
    
    wanted_data = get_wanted_list()
    return render(request, 'HomePage.html',{'wanted_list': wanted_data,})

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
    # if request.method == 'POST':
    #     return redirect
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
                # 'reporter': str(case.reporter.user_name), 
                # "reporter_pic":str(case.reporter.user_profile_picture.url),# convert ForeignKey to string or ID
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
           
        data['case_data']=(case_data)
        
        evidences = Evidence.objects.filter(case=case)
        evidence_Data=dict()
            
        for evidence in evidences:
        #    append into the evidence_Date dictionary
            evidence_Data[evidence.id] = {
                'evidence_id': evidence.id,
                'evidence_type': evidence.evidence_type,
                'evidence_pic_file': str(evidence.evidence_pic_file.url) if evidence.evidence_pic_file else None,
                'evidence_vid_file': str(evidence.evidence_vid_file.url) if evidence.evidence_vid_file else None, 
            }
            
        data['evidence'] = evidence_Data
        
        citizenship = Cp.objects.filter(user=case.reporter)
        citizenship_Data = dict()
        for citizen in citizenship:
            citizenship_Data[citizen.id] = {
                'citizenship_id': citizen.id,
                'citizenship_photo': str(citizen.citizenship_photo.url) if citizen.citizenship_photo else None,
            }

        data['citizenship'] = citizenship_Data
        
        reporter_recent_photo = case.reporter.user_recent_photo.url if case.reporter.user_recent_photo else None
        
        data['recent_photo'] = {
            'recent_photo' : reporter_recent_photo
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
        
        case = Case.objects.get(case_id = id)
        
        print(case,activity_name,activity_description,activity_file)
        activity_log = Activity_log(case=case,activity_title=activity_name,activity_description=activity_description)
        activity_log.save()
        
        if activity_file:
            save_evidence(activity_file,case) # Imported from Citizen.Views
        return JsonResponse({"status":"success"})
        # print(activity_name,activity_description,activity_file)
 
def fetch_activity_log(request,id):
    case = Case.objects.get(case_id = id)
    activity_log = Activity_log.objects.filter(case=case).values('activity_title','activity_description','activity_date')
    activity_log = list(activity_log)      
    return JsonResponse(activity_log, safe=False)
    
        
    

