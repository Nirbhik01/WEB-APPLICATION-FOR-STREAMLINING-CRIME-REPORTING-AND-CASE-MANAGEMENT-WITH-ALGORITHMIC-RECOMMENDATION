from django.shortcuts import render, redirect
from django.contrib import messages
from userauths.models import Citizen, Investigator
from django.contrib.sessions.models import Session
from Citizen.views import register_case

from django.http import JsonResponse
# from ReportEaseApp.views import HomePage
# from django.http import JsonResponse
import uuid

def redirect_to_login(request):
    return redirect('/user/login/')

def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # "Citizen" or "Investigator"

        if not email or not password or not user_type:
            messages.error(request, "All fields are required.")
            return redirect('userauths:LoginPage')

        user = None
        if user_type == 'Citizen':
            try:
                user = Citizen.objects.get(user_email=email)
                if not user.verify_password(password):  # Check hashed password
                    messages.error(request, "Incorrect password.")
                    return redirect('userauths:LoginPage')
                request.session['user_id'] = user.user_id  # Store user ID
                request.session['user_type'] = 'Citizen' 
               
            except Citizen.DoesNotExist:
                messages.error(request, "Citizen account with this email does not exist.")
                return redirect('userauths:LoginPage')
        
        elif user_type == 'Investigator':
            try:
                user = Investigator.objects.get(user_email=email)
                if not user.verify_password(password):
                    messages.error(request, "Incorrect email or password.")
                    return redirect('userauths:LoginPage')
                request.session['user_id'] = user.user_id  # Store user ID
                request.session['user_type'] = 'Investigator'
                
            except Investigator.DoesNotExist:
                messages.error(request, "Investigator account with this email does not exist.")
                return redirect('userauths:LoginPage')
        
        else:
            messages.error(request, "Invalid user type selected.")
            return redirect('userauths:LoginPage')

        

        return redirect('ReportEaseApp:HomePage')

    return render(request, 'LoginPage.html')


def RegisterPage(request):
    if request.method=='POST':
        if request.POST.get('register_user_form') == 'register_user_form':
            user_type = request.POST.get('registerAs')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            address = request.POST.get('address')
            phone = int(request.POST.get('number'))
        
            profile_pic = request.FILES['profile_pic']
            
            # check if email already exists
            
            
            if user_type == 'Citizen':
                check_email =  Citizen.objects.filter(user_email=email).exists()
                if check_email:
                    messages.error(request, "Email already exists.")
                    return JsonResponse({"status": "error", "message": "Email already exists."})
                user = Citizen(user_name=fname + " " + lname, user_email=email, user_password=password, user_address=address, user_phone_number=phone,user_profile_picture=profile_pic)
                user.save()
                messages.success(request, "Citizen registered successfully.")
                # return redirect('userauths:LoginPage')
                return JsonResponse({"status": "success"})
            elif user_type == 'Investigator':
                district = request.POST.get('district')
                check_email =  Investigator.objects.filter(user_email=email).exists()
                if check_email:
                    messages.error(request, "Email already exists.")
                    return JsonResponse({"status": "error", "message": "Email already exists."})
                user = Investigator(user_name=fname + " " + lname, user_email=email, user_password=password, user_address=address, user_phone_number=phone, user_district=district,user_profile_picture=profile_pic)
                user.save()
                messages.success(request, "Investigator registered successfully.")
                # return redirect('userauths:LoginPage')
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Registration Failed"})
        elif request.POST.get('register_crime_form') == 'register_crime_form':
            if register_case(request):
                messages.success(request, "Case registered successfully.")
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Registration Failed"})
        
    return render(request, 'RegisterPage.html')


def LogoutPage(request):
    request.session.clear()
    return redirect('/user/login/')

# Create your views here.
