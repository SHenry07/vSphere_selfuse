import xadmin
from .models import Vsphere
# Register your models here.
class VsphereAdmin(object):

    list_display = ('vsphere_comment','vsphere_host')
    
xadmin.site.register(Vsphere,VsphereAdmin)