from django.shortcuts import render

from django.http import JsonResponse
from .models import Wanted

def get_wanted_list():
    # Fetch the list of wanted individuals from the database and 
    wanted_list = Wanted.objects.all().values('wanted_name', 'wanted_reason', 'wanted_pic','upload_date')
    # sort wanted list by upload_date so that recent date comes first
    wanted_list = wanted_list.order_by('-upload_date')
    
    # Convert the queryset to a list of dictionaries
    wanted_list = list(wanted_list)
    
    return list(wanted_list)
# Create your views here.
