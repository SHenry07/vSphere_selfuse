from django.shortcuts import render , get_object_or_404,get_list_or_404

from django.http import HttpResponse , HttpResponseRedirect

from .models import Vsphere,Disk,VmDetails

from vsphere_exec.add_disk_to_vm import add_disk

from vsphere_exec.get_args import service_con, Get_Vm
from vsphere_exec.virtual_machine_device_info import Device_Info 
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
    vm_ips = get_object_or_404(Vsphere,pk=vsphere_comment)
     #初始化变量
    host = vm_ips.vsphere_host
    user = vm_ips.vsphere_username
    pwd  = vm_ips.vsphere_password
    result = result1 = result2 = {}

    #调用外部函数 
    si = service_con(host,user,pwd)
    print(type(request.POST))
    if request.POST:
        print(request.POST['ipaddress'])
        print(request.POST['vmname'])
        vm_ip=request.POST['ipaddress']
        vm_name =request.POST['vmname']
        UUID=request.POST['uuid']
        disk_size=request.POST['size']
        if vm_ip or vm_name: 
            vm = Get_Vm(si,vm_name=vm_name,vm_ip=vm_ip)
            result=Device_Info(vm)
            result1 = result[0]
            result2 = result[1]
            
            context = {
                'vm_ips':vm_ips,
                'result1':result1,
                'result2':result2,
            }
        elif UUID and disk_size:
            vm= Get_Vm(si,vm_uuid=UUID)
            add_disk_action = add_disk(vm,si,disk_size)
            context= {
             'vm_ips':vm_ips,
             'adddiskaction':add_disk_action,
            }
    else:
        context = {'vm_ips':vm_ips}
    return render(request,'adddisk/machines.html',context)


#def machines(request,vsphere_comment):
#    #get_object_or_404(klass,*args,**kwarg) Klass可以使一个Model class，一个manager
#    #暂时不明或者一个QuerySet 迭代器 **kwarg get()或者filter()支持的类型都可以
#    vm_ips = get_object_or_404(Vsphere,pk=vsphere_comment)
#    
#    try:
#        #初始化变量
#        host = vm_ips.vsphere_host
#        user = vm_ips.vsphere_username
#        pwd  = vm_ips.vsphere_password
#        result = result1 = result2 = {}
#
#        #调用外部函数 
#        si = service_con(host,user,pwd)
#        vm_ip=request.POST['ipaddress']
#        vm_name =request.POST['vmname']
#
#    except :
#        return render(request,'adddisk/machines.html',{
#            'vm_ips':vm_ips,
#            "error_message":"Not found the machine.",
#        })
#    else:
#        vm = Get_Vm(si,vm_name=vm_name,vm_ip=vm_ip)
#        result=Device_Info(vm)
#        result1 = result[0]
#        result2 = result[1]
#        context = {
#            'vm_ips':vm_ips,
#            'result1':result1,
#            'result2':result2,
#        }
#        if vm_ip:
#            return HttpResponseRedirect(reversed('adddisk:vmdetail',args=(vsphere_comment,)),context)
#        elif vm_name:
#            return HttpResponseRedirect(reversed('adddisk:vmdetail',args=(vsphere_comment,)),context)


def details(request,vsphere_comment,vm_name=None,vm_ip=None):
    vm_info = get_object_or_404(VmDetails, vm_name=vm_name)
    vm_ips = get_object_or_404(Vsphere,pk=vsphere_comment)
    host = vm_ips.vsphere_host
    user = vm_ips.vsphere_username
    pwd  = vm_ips.vsphere_password
    result = {}
    if request.POST:
        si = service_con(host,user,pwd)
        disk_size=request.POST['size']
        result = add_disk(vm_name,si,disk_size)
    context = {
        'vm_info':vm_info,
        'result':result,
    }
    return render(request,'adddisk/detail.html',context)
