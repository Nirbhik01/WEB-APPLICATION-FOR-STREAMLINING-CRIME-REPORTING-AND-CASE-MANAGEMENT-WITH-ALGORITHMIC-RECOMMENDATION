from django.shortcuts import render,redirect
from django.contrib import messages
# from userauths.views import get_current_user



def LandingPage(request):
    return render(request, 'LandingPage.html')

def HomePage(request):
    login_check = check_for_login(request)
    if login_check:
        return login_check
    return render(request, 'HomePage.html')

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

def CasePage(request):
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
    print("entered inside check login")
    try:
        print("entered inside try")
        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')
        if not(user_id and user_type):
            print("entered inside if")
            messages.warning(request,"You must be logged in to view that page")
            return redirect('userauths:LoginPage')
    except:
        print("entered inside except")
        messages.warning(request,"You must be logged in to view that page")
        return redirect('userauths:LoginPage')

# Create your views here.




