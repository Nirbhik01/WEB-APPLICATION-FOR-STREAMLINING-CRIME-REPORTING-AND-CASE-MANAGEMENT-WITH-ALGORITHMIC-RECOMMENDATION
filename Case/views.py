from django.shortcuts import render

from django.http import JsonResponse
from .models import *

def get_wanted_list():
    # Fetch the list of wanted individuals from the database and 
    wanted_list = Wanted.objects.all().values('wanted_name', 'wanted_reason', 'wanted_pic','upload_date')
    # sort wanted list by upload_date so that recent date comes first
    wanted_list = wanted_list.order_by('-upload_date')
    
    # Convert the queryset to a list of dictionaries
    wanted_list = list(wanted_list)
    
    return list(wanted_list)

def fetch_cases(request):
    
    case_list = Case.objects.all().values('case_title','upload_date', 'crime_description','case_id','reporter__user_profile_picture','reporter__user_name')
    
    # case_list = case_list.order_by('-crime_date')
    
    # Convert the queryset to a list of dictionaries
    case_list = list(case_list)
    
    return JsonResponse(case_list, safe=False)

def search_cases(request):
    query = request.GET.get('q', '')
    cases = None
    if query:
        # Search logic (case-insensitive)
        cases = Case.objects.filter(case_title__icontains=query).values('case_title','upload_date', 'crime_description','case_id','reporter__user_profile_picture','reporter__user_name')
    # Fetch the list of cases from the database and also the reporters profile pic path
    return JsonResponse(list(cases), safe=False)

def filter_cases(request):
    pass
# Create your views here.
