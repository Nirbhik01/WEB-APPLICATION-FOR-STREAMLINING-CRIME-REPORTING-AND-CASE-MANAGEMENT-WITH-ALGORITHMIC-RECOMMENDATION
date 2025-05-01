from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from Case.models import Case,Evidence,Wanted
from userauths.models import Citizen as Ct
from Case.views import display_cases
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
        data=dict()
        case = Case.objects.get(case_id=id)
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
        
        
        
        data['evidence']=(evidence_Data)
        
        reporter_recent_photo = case.reporter.user_recent_photo.url if case.reporter.user_recent_photo else None
        
        data['recent_photo'] = {
            'recent_photo': reporter_recent_photo
        }
            
        return JsonResponse(data, safe=False)
    
    
    except Case.DoesNotExist:
        return JsonResponse({"error": "Case not found"}, status=404)

def get_wanted_list():
    # Fetch the list of wanted individuals from the database 
    wanted_list = Wanted.objects.all().values('wanted_name', 'wanted_reason', 'wanted_pic','upload_date')
    # sort wanted list by upload_date so that recent date comes first
    wanted_list = wanted_list.order_by('-upload_date')
    
    # Convert the queryset to a list of dictionaries
    wanted_list = list(wanted_list)
    
    return (wanted_list)



