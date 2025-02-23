from userauths.models import Citizen, Investigator

def user_context(request):
    user = None
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if user_id and user_type:
        try:
            if user_type == 'Citizen':
                user = Citizen.objects.get(citizen_id=user_id)
                # print(f"found citizen \n {user.citizen_profile_picture}  \n {user.citizen_name}")
                
            elif user_type == 'Investigator':
                user = Investigator.objects.get(investigator_id=user_id)
                # print("found Investigator")
        except (Citizen.DoesNotExist, Investigator.DoesNotExist):
            print("not found user")  # User might have been deleted

    return {'logged_in_user': user, 'user_type': user_type}
