from userauths.models import Citizen, Investigator
from django.shortcuts import render,redirect

def user_context(request):
    user_id=None
    user_type=None
    try:
        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')
        print(user_type,user_id)
    except:
        return redirect("userauths:LoginPage")
    user = None
    if user_id and user_type:
        try:
            if user_type == 'Citizen':
                user = Citizen.objects.get(user_id=user_id)
                # print(f"found citizen \n {user.citizen_profile_picture}  \n {user.citizen_name}")
                
            elif user_type == 'Investigator':
                user = Investigator.objects.get(user_id=user_id)
            
            # for admin
            elif user_type == 'admin':
                user = request.user
                # print("found Investigator")
        except (Citizen.DoesNotExist, Investigator.DoesNotExist):
            print("not found user")  # User might have been deleted

    return {'logged_in_user': user, 'user_type': user_type}
