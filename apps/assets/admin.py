from django.contrib import admin
from .models import VmDetails
# Register your models here.


class VmDetailsAdmin(admin.ModelAdmin):
    # 改变后台手动添加的界面
    # fields = ['vm_name','vm_instance_UUID','datacenter']
    # fieldsets = [
    #     ('虚拟机名字',  {'fields': ['vm_name']}),
    #     ('唯一UUID',   {'fields': ['vm_instance_UUID']}),
    #     ('iDC',        {'fields': ['datacenter']}),
    # ]
    
    # 改变后台展示
    list_display = ('vm_name','vm_ip','vm_guest_username','vm_password','department','vm_instance_UUID',
    'tags','datacenter')
    search_fields = ('vm_name','vm_ip')
admin.site.register(VmDetails,VmDetailsAdmin)
