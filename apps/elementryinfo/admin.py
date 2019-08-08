from django.contrib import admin

from .models import Vsphere
# Register your models here.
class VsphereAdmin(admin.ModelAdmin):

    list_display = ('vsphere_comment','vsphere_host')
    
admin.site.register(Vsphere,VsphereAdmin)