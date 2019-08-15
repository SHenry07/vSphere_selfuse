'''
@Description: 
@Author: Henry Sun
@Date: 2019-08-07 14:11:06
@LastEditors: Henry Sun
@LastEditTime: 2019-08-15 08:37:10
'''
import xadmin
from .models import VmDetails
# Register your models here.


class VmDetailsAdmin(object):
    # 改变后台手动添加的界面
    # fields = ['vm_name','vm_instance_UUID','datacenter']
    # fieldsets = [
    #     ('虚拟机名字',  {'fields': ['vm_name']}),
    #     ('唯一UUID',   {'fields': ['vm_instance_UUID']}),
    #     ('iDC',        {'fields': ['datacenter']}),
    # ]
    
    # 改变后台展示
    list_display = ('datacenter','vm_name','vm_ip','vm_guest_username','vm_password','department','vm_instance_UUID',
    'tags','m_time')
    search_fields = ('vm_name','vm_ip')
    list_filter = ['datacenter', 'tags', 'department']
    list_editable = ["tags", "department"]
xadmin.site.register(VmDetails,VmDetailsAdmin)

