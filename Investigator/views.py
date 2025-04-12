from django.shortcuts import render,redirect
# import messages
from django.contrib import messages
from django.http import JsonResponse
from Case.models import Wanted as Wt

# Create your views here.
def UploadWanted(request):
    
    if request.method == 'POST':
        name = request.POST.get('Wanted_name')
        wanted_for = request.POST.get('Wanted_for')
        wanted_pic = request.FILES['Wanted_photo'] 
        
        # Create a new Wanted object and save it to the database
         
        wanted_post = Wt(
            wanted_name = name,
            wanted_reason = wanted_for,
            wanted_pic = wanted_pic
        )
        wanted_post.save()
        # messages.success(request, 'Wanted Post Created Successfully!')
        messages.success(request, 'Wanted Post Created Successfully!')
        # return JsonResponse({"status": "success", "message": "Wanted Post Created."})
        return redirect("ReportEaseApp:HomePage")
    # Change 'success_page' to your desired URL or view name
    
    return JsonResponse({"status":"error","message":"An error occured"})  # Render the upload form template