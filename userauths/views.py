from django.shortcuts import render, redirect
from django.contrib import messages
from userauths.models import Citizen, Investigator
from django.contrib.sessions.models import Session
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
            return redirect('/user/login')

        user = None
        if user_type == 'Citizen':
            try:
                user = Citizen.objects.get(citizen_email=email)
                if not user.verify_password(password):  # Check hashed password
                    messages.error(request, "Incorrect password.")
                    return redirect('/user/login')
                request.session['user_id'] = user.citizen_id  # Store user ID
                request.session['user_type'] = 'Citizen' 
               
            except Citizen.DoesNotExist:
                messages.error(request, "Citizen account with this email does not exist.")
                return redirect('/user/login')
        
        elif user_type == 'Investigator':
            try:
                user = Investigator.objects.get(investigator_email=email)
                if not user.verify_password(password):
                    messages.error(request, "Incorrect email or password.")
                    return redirect('/user/login')
                request.session['user_id'] = user.investigator_id  # Store user ID
                request.session['user_type'] = 'Investigator'
                
            except Investigator.DoesNotExist:
                messages.error(request, "Investigator account with this email does not exist.")
                return redirect('/user/login')
        
        else:
            messages.error(request, "Invalid user type selected.")
            return redirect('/user/login')

        # If login is successful
        request.session['user_email'] = email
        request.session['user_type'] = user_type
        
        # messages.success(request, f'Welcome, {user.citizen_name if user_type == "Citizen" else user.investigator_name}!')
        return redirect(f'/home/')

    return render(request, 'LoginPage.html')




def RegisterPage(request):
    return render(request, 'RegisterPage.html')

# Create your views here.
