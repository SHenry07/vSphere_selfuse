from django.contrib import admin

from .models import Vsphere,VmDetails,Disk
#Register your models here.

admin.site.register(Vsphere)
admin.site.register(VmDetails)
