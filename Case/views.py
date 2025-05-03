from django.shortcuts import render,redirect
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime, time
from userauths.models import Citizen as Ct, Investigator as Iv


from django.http import JsonResponse
from .models import *

def fetch_cases(request):
    
    case_list = Case.objects.filter(is_registered=False).values('case_title','upload_date', 'crime_description','case_id','reporter__user_profile_picture','reporter__user_name','is_registered')
    
    # case_list = case_list.order_by('-crime_date')
    
    # Convert the queryset to a list of dictionaries
    case_list = list(case_list)
    
    return JsonResponse(case_list, safe=False)

def search_cases(request):
    query = request.GET.get('q', '')
    # make a list of words in the query separated by spaces
    query = query.split()
    cases = []
    seen_case_ids = set() 
    if query:
        for search_term in query:
            matched_cases = list(Case.objects.filter(
                case_title__icontains=search_term,is_registered=False
            ).values(
                'case_title', 'upload_date', 'crime_description',
                'case_id', 'reporter__user_profile_picture', 'reporter__user_name'
            ))  
            
            for case in matched_cases:
                if case['case_id'] not in seen_case_ids:
                    seen_case_ids.add(case['case_id'])
                    cases.append(case)
            
    return JsonResponse(cases, safe=False)

def filter_cases(request):
    if request.method=="POST":  
        from_date_str=request.POST.get('startDate') if request.POST.get('startDate') else None
        to_date_str=request.POST.get('endDate') if request.POST.get('endDate') else None
        crime_type = request.POST.get('crime_type') if request.POST.get('crime_type') else None
        
        from_date = None
        to_date = None
        
        if from_date_str:
            from_date = parse_date(from_date_str)

        if to_date_str:
            to_date = parse_date(to_date_str)
            
        case_list = Case.objects.filter(is_registered=False)

        if from_date:
            case_list = case_list.filter(upload_date__date__gte=from_date)
        if to_date:
            case_list = case_list.filter(upload_date__date__lte=to_date)
        if crime_type:
            case_list = case_list.filter(case_title=crime_type)

        case_list = case_list.values(
            'case_title', 'upload_date', 'crime_description', 'case_id',
            'reporter__user_profile_picture', 'reporter__user_name'
        )
            
        return JsonResponse(list(case_list), safe=False)
          
def display_cases(request):
    print("entered diaplay cases")
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    
    if user_type == 'Citizen':
        print("entered citizen")
        user = Ct.objects.get(user_id=user_id)
        print(user)
        cases = Case.objects.filter(reporter=user, is_reporter_the_victim = True).exclude(
                                            status='Investigation_Termination').values('case_id','case_title','investigator','status')
        print(list(cases))
        return JsonResponse(list(cases), safe=False)
    
    elif user_type == 'Investigator':
        print("entered investigator")
        user = Iv.objects.get(user_id=user_id)
        cases = Case.objects.filter(investigator=user,is_registered=True).exclude(
                                            status='Investigation_Termination').values('case_id','case_title','reporter','status')
        return JsonResponse(list(cases), safe=False)
    
    return JsonResponse({"status": "error", "message": "An error Occured"})    

  
# Create your views here.
