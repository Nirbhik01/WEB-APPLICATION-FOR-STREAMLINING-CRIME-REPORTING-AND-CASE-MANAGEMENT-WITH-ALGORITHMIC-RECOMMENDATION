from django.shortcuts import render, redirect
from django.contrib import messages
from userauths.models import Citizen, Investigator
from django.contrib.sessions.models import Session
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

        
        # session_key = str(uuid.uuid4())
        # request.session['session_key'] = session_key
        # print(session_key)
        # # Store user data separately for each tab's session_key
        # if user_type == 'Investigator':
        #     request.session["user_id_" + session_key] = user.investigator_id
            
        # elif user_type == 'Citizen':
        #     request.session["user_id_" + session_key] = user.citizen_id
        # request.session.modified = True
        
        print(request.session.items())
        # messages.success(request, f'Welcome, {user.citizen_name if user_type == "Citizen" else user.investigator_name}!')
        return redirect('ReportEaseApp:HomePage')

    return render(request, 'LoginPage.html')


def RegisterPage(request):
    return render(request, 'RegisterPage.html')


def LogoutPage(request):
    request.session.clear()
    return redirect('/user/login/')

# Create your views here.
