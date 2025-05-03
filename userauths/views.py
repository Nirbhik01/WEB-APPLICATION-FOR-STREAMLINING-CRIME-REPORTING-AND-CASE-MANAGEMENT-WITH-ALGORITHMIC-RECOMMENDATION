from django.shortcuts import render, redirect
from django.contrib import messages
from userauths.models import Citizen, Investigator
import random
from django.contrib.auth import authenticate, login

from django.http import JsonResponse

# for email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def redirect_to_login(request):
    return redirect('/user/login/')

def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # "Citizen" or "Investigator" or "Admin"

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
            
        elif user_type == "Admin":
            try:
                user = authenticate(request, username=email, password=password)
                if user is not None and user.is_superuser:
                    login(request, user)  # logs in using Django session
                    request.session['user_id'] = user.id
                    request.session['user_type'] = 'Admin'
                else:
                    messages.error(request, "Error logging in with admin credentials.")
                    return redirect('userauths:LoginPage')
            except:
                pass
        else:
            messages.error(request, "Invalid user type selected.")
            return redirect('userauths:LoginPage')

        return redirect('ReportEaseApp:HomePage')

    return render(request, 'LoginPage.html')

def RegisterPage(request):
    if request.method=='POST':
        
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
                check_email =  (Citizen.objects.filter(user_email=email).exists() or Investigator.objects.filter(user_email=email).exists())
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
                check_email =  (Investigator.objects.filter(user_email=email).exists() or Citizen.objects.filter(user_email=email).exists())
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
    
    return render(request, 'RegisterPage.html')

def ForgotPasswordPage(request):
    return render(request, 'ForgotPasswordPage.html')

def LogoutPage(request):
    request.session.clear()
    return redirect('/user/login/')

def send_otp(request):
    if request.method=='POST':
        email = request.POST.get('email')
        print(email)
        try:
            user = Citizen.objects.get(user_email=email) if Citizen.objects.filter(user_email=email).exists() else None
            if not user:
                user = Investigator.objects.get(user_email=email) if Investigator.objects.filter(user_email=email).exists() else None
            if not user:
                return JsonResponse({'status': 'fail', 'message': 'Email not found'}, status=404)
            otp = random.randint(100000, 999999)
            request.session['reset_email'] = email
            request.session['reset_otp'] = str(otp)
            
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()

            # Login using your Gmail app password
            s.login("dhakaln76@gmail.com", "ttuc lfxu ruti zgxp")  # Replace with your App Password
            
            msg = MIMEMultipart("alternative")
            msg['From'] = "dhakaln76@gmail.com"
            msg['To'] = f"{request.session.get('reset_email')}"
            msg['Subject'] = f"OTP Verification"

            # Plain text version (optional)
            text = f""".
                    """

            # HTML version
            html = f"""
            <html>
            <body>
                <h2 style="color:#2C3E50;">Hello, {user.user_name}!</h2>
                <p>Your OTP is <b>{request.session.get("reset_otp")}</b> <br/> This is an OTP to change your profile password for ReportEase.
                    Do not share this with anyone. </p>
            </body>
            </html>
            """

            # Attach both plain and HTML parts
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            msg.attach(part1)
            msg.attach(part2)

            # Send the email
            s.sendmail(msg['From'], msg['To'], msg.as_string())

            # Quit the SMTP session
            s.quit()
            return JsonResponse({'status': 'success'})
        except: 
            return JsonResponse({'status': 'fail', 'message': 'There was a problem sending email'}, status=404)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=405)

def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        session_otp = request.session.get('reset_otp')

        if int(otp_input) == int(session_otp):
            request.session['otp_verified'] = True
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'fail', 'message': 'Invalid OTP'})
    return JsonResponse({"status": "fail", "message": "Invalid request Method"},status=400)

def change_password(request):
    if not request.session.get('otp_verified'):
        print("OTP not verified")
        return JsonResponse({'status': 'fail', 'message': 'OTP not verified'}, status=403)

    password = request.POST.get('password')
    cpassword = request.POST.get('cpassword')

    if password != cpassword:
        return JsonResponse({'status': 'fail', 'message': 'Passwords do not match'}, status=400)

    try:
        email = request.session.get('reset_email')
        user = Citizen.objects.get(user_email=email) if Citizen.objects.filter(user_email=email).exists() else None
        if not user:
            user = Investigator.objects.get(user_email=email) if Investigator.objects.filter(user_email=email).exists() else None
        user.user_password = password
        user.save()

        # Cleanup session
        del request.session['reset_email']
        del request.session['reset_otp']
        del request.session['otp_verified']

        messages.success(request, "Password changed successfully.")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)
# Create your views here.
