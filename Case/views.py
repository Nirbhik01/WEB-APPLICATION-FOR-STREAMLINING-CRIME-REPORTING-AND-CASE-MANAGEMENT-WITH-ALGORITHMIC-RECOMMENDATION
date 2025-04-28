from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime, time

from django.http import JsonResponse
from .models import *

def get_wanted_list():
    # Fetch the list of wanted individuals from the database 
    wanted_list = Wanted.objects.all().values('wanted_name', 'wanted_reason', 'wanted_pic','upload_date')
    # sort wanted list by upload_date so that recent date comes first
    wanted_list = wanted_list.order_by('-upload_date')
    
    # Convert the queryset to a list of dictionaries
    wanted_list = list(wanted_list)
    
    return list(wanted_list)

def fetch_cases(request):
    
    case_list = Case.objects.filter(is_registered=False).values('case_title','upload_date', 'crime_description','case_id','reporter__user_profile_picture','reporter__user_name')
    
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
                
# Create your views here.
