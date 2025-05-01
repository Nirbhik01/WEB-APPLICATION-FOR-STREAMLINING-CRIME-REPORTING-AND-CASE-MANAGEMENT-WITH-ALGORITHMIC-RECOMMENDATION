from django.shortcuts import render,redirect
# import messages
from django.contrib import messages
from django.http import JsonResponse
from Case.models import Wanted as Wt
from Case.models import Case, Evidence


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


    
def mark_case_registered(request,id):
    try:
        case = Case.objects.get(case_id=id)
        case.is_registered = True
        case.status = "Investigator_Assigning"
        case.save()
        messages.success(request,"Case marked as Registered")
        return JsonResponse({"status": "success"})
    except Case.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Case not found."})
    
def mark_case_not_registered(request,id):
    try:
        # delete case from db
        case = Case.objects.get(case_id=id)
        
        
        # also delete all its associated files from their respective paths
        evidences = Evidence.objects.filter(case=case)
        for evidence in evidences:
            if evidence.evidence_pic_file:
                evidence.evidence_pic_file.delete()
            if evidence.evidence_vid_file:
                evidence.evidence_vid_file.delete()
        
        case.delete()
        
        messages.success(request,"Case Removed Successfully")
        return JsonResponse({"status": "success"})
    
    except:
        return JsonResponse({"status": "error", "message": "Operation Failed"})
 
# Create your views here.