'''
@Description: 自定义过滤器
@Author: Henry Sun
@Date: 2019-08-15 09:00:03
@LastEditors: Henry Sun
@LastEditTime: 2019-08-15 09:13:54
'''

import django_filters

from .models import VmDetails


class VmDetailsFilter(django_filters.FilterSet):
    """
    虚拟机信息过滤
    """

    class Meta:
        model = VmDetails
        fields = ['vm_name','vm_ip','vm_instance_UUID', 'department', 'datacenter', 'vm_cpu', 
                'vm_memory', 'm_time']