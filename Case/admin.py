from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Case)
admin.site.register(Evidence)
admin.site.register(Activity_log)  
admin.site.register(Wanted)