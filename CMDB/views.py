from django.shortcuts import render , get_object_or_404,get_list_or_404

from django.http import HttpResponse

from .models import Vsphere,Disk,VmDetails
# Create your views here.

def index(request):
    #return HttpResponse("You're in %s %d" % vsphere_comment, vsphere_host)
    datacenter_list = Vsphere.objects.order_by('-vsphere_host')[::]
    context = {
        'datacenter_list':datacenter_list,
    }
    #return HttpResponse("Please pick the datacenter: %s " % output)
    return render(request,'cmdb/index.html', context)


def machines(request,vsphere_comment):
    #get_object_or_404(klass,*args,**kwarg) Klass可以使一个Model class，一个manager
    #暂时不明或者一个QuerySet 迭代器 **kwarg get()或者filter()支持的类型都可以
    vm_ips = get_object_or_404(Vsphere,pk=vsphere_comment)
    return render(request,'cmdb/machines.html',{'vm_ips':vm_ips})

def details(request,vsphere_comment,vm_name):
    vm_info = get_object_or_404(VmDetails, vm_name=vm_name)
    return render(request,'cmdb/detail.html',{ 'vm_info': vm_info })

