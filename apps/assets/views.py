from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import VmDetails
# Create your views here.

def dashboard(request):
    pass
    return render(request,'assets/dashboard.html', locals())

def VMDeatilsAll(request):
    '''
    @description:展示所有主机 
    @param {type} 
    @return: 
    '''
    allvm = VmDetails.objects.all()
    
    return render(request,'assets/vmall.html',locals())
    

def VMDeatilsEachIDC(request,vsphere_comment):
    """
    :param request:
    :param vsphere_comment 9f hcbanksteel:
    :return:
    """
    allvmEachIDC = VmDetails.objects.filter(datacenter=vsphere_comment)
    
    return render(request,'assets/vmeachIDC.html',locals())


def vmdetailsOne(request,UUID):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param UUID:
    :return:
    """
    pass