from django.shortcuts import render , get_object_or_404,get_list_or_404

from django.http import HttpResponse

from .models import Vsphere,Disk,VmDetails

from vsphere_exec.add_disk_to_vm import *

from vsphere_exec.get_args import *
# Create your views here.

def index(request):
    #return HttpResponse("You're in %s %d" % vsphere_comment, vsphere_host)
    datacenter_list = Vsphere.objects.order_by('-vsphere_host')[::]
    context = {
        'datacenter_list':datacenter_list,
    }
    #return HttpResponse("Please pick the datacenter: %s " % output)
    return render(request,'adddisk/index.html', context)


def machines(request,vsphere_comment):
    #get_object_or_404(klass,*args,**kwarg) Klass可以使一个Model class，一个manager
    #暂时不明或者一个QuerySet 迭代器 **kwarg get()或者filter()支持的类型都可以
    vm_ips = get_object_or_404(Vsphere,pk=vsphere_comment)
    return render(request,'adddisk/machines.html',{'vm_ips':vm_ips})

def details(request,vsphere_comment,vm_name):
    vm_info = get_object_or_404(VmDetails, vm_name=vm_name)
    vm_ips = get_object_or_404(Vsphere,pk=vsphere_comment)
    host = vm_ips.vsphere_host
    user = vm_ips.vsphere_username
    pwd  = vm_ips.vsphere_password
    si = service_con(host,user,pwd)
    if request.POST:
        disk_size=request.POST['size']
        result = add_disk(vm_name,si,disk_size)
    context = {
        'vm_info':vm_info,
        'result':result,
    }
    return render(request,'adddisk/detail.html',context)
