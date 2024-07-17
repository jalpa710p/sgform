from django.contrib import admin
from  signupform.models import  Sgform
# Register your models here.

@admin.register(Sgform)
class sgformadmin(admin.ModelAdmin) :
    list_display = ['usn','phn','eml','psd']