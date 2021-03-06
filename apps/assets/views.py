'''
@Description: 
@Author: Henry Sun
@Date: 2019-08-07 14:11:06
@LastEditors: Henry Sun
@LastEditTime: 2019-08-15 10:49:12
'''
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import VmDetails
from .filters import VmDetailsFilter
# Create your views here.

def dashboard(request):
    total = VmDetails.objects.count()
    upline = VmDetails.objects.filter(powerstate="On").count()
    offline = VmDetails.objects.filter(powerstate="Off").count()
    nicup = VmDetails.objects.filter(NICstate="On").count()
    nicoff = VmDetails.objects.filter(NICstate="Off").count()
    nicnotuse = VmDetails.objects.filter(NICstate="Unused").count()

    up_rate = round(upline / total*100)
    off_rate = round(offline / total * 100)
    nicup_rate = round(nicup / total * 100)
    nicoff_rate = round(nicoff / total * 100)
    nicnu_rate = round(nicnotuse / total * 100)

    return render(request, 'assets/dashboard.html', locals())

def VMDeatilsAll(request):
    '''
    @description:展示所有主机 
    @param {type} 
    @return: 
    '''
    allvm = VmDetailsFilter(request.GET,queryset=VmDetails.objects.all())
    # allvm = VmDetails.objects.all()
    return render(request, 'assets/vmall.html', {'allvm' : allvm})
    

def VMDeatilsEachIDC(request,vsphere_comment):
    """
    :param request:
    :param vsphere_comment 9f hcbanksteel:
    :return:
    """
    allvmEachIDC = VmDetails.objects.filter(datacenter=vsphere_comment)
    
    return render(request, 'assets/vmeachIDC.html', locals())


def vmdetailsOne(request,UUID):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param UUID:
    :return:
    """
    vm = get_object_or_404(VmDetails,vm_instance_UUID=UUID)
    return render(request, 'assets/details.html', locals())


def report(request):
    '''
    @description: 
    @param {type} 
    @return: 
    '''

    pass 