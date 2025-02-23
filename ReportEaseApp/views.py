from django.shortcuts import render,redirect

def LandingPage(request):
    return render(request, 'LandingPage.html')

# def LoginPage(request):
#     return render(request, 'LoginPage.html')


# def RegisterPage(request):
#     return render(request, 'RegisterPage.html')

def HomePage(request):
    return render(request, 'HomePage.html')

def UploadWantedPage(request):
    return render(request, 'UploadWantedPage.html')

def ReviewFirPage(request,id):
    return render(request, 'ReviewFirPage.html')

def CaseListPage(request):
    return render(request, 'CaseListPage.html')

def CasePage(request):
    # if request.method == 'POST':
    #     return redirect
    return render(request, 'CasePage.html')

def ReportCrimePage(request):

    return render(request, 'ReportCrimePage.html')

def ProfilePage(request):
    return render(request, 'ProfilePage.html')

def CaseListPage(request):
    return render(request, 'CaseListPage.html')
# Create your views here.




