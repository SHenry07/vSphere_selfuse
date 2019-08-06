from __future__ import absolute_import, unicode_literals

from django.shortcuts import render , get_object_or_404,get_list_or_404
from django.http import HttpResponse , HttpResponseRedirect

from time import ctime
import request
import simplejson as json
import logging ; logging.basicConfig(level=logging.INFO)

from .models import Vsphere
from .task import CloneDelay
from vsphere_exec.add_disk_to_vm import add_disk
from vsphere_exec.get_args import service_con, Get_Vm
from vsphere_exec.virtual_machine_device_info import Device_Info
from vsphere_exec.clone_vm import  clone_vm

# Create your views here.

def idc(request):
    datacenter_list = Vsphere.objects.order_by('-vsphere_comment')[::]
    context = {
        'datacenter_list':datacenter_list,
    }
    # 初始化页面
    return render(request,'clonevm/idc.html', context)


def machines(request,vsphere_comment):
    """
    IP或者VM_name 调用查询模块
    instant UUID 和 capacity 调用加硬盘模块
    :param request post:
    :param vsphere_comment:
    :return:
    """
    vm_ips = get_object_or_404(Vsphere,pk=vsphere_comment)
     #初始化变量
    host = vm_ips.vsphere_host
    user = vm_ips.vsphere_username
    pwd  = vm_ips.vsphere_password
    result = result1 = result2 = {}

    #调用外部vsphere函数 
    try:
        si = service_con(host,user,pwd)
        if request.POST:
            vm_ip=request.POST['ipaddress']
            vm_name =request.POST['vmname']
            UUID=request.POST['uuid']
            disk_size=request.POST['size']
            if vm_ip or vm_name:
                """
                字典格式
                """
                vm = Get_Vm(si,vm_name=vm_name,vm_ip=vm_ip)
                if type(vm) == str:
                    raise TypeError
                result  = Device_Info(vm)
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
                if type(vm) == str:
                    raise TypeError
                context= {
                    'vm_ips':vm_ips,
                    'adddiskaction':add_disk_action,
                }
        else:
            # 防止刷新 无返回值
            context = {'vm_ips':vm_ips}
        return render(request,'clonevm/machines.html',context)
    except OSError :
        return HttpResponse("<p>无法连接远程vsphere服务器</p>")
    except TypeError :
        return HttpResponse("<p>无此虚拟机或虚拟机不受Vmtools控制，请尝试用VM名字来搜索</p>")
       # 要实现自动跳转回主页面

#def machines(request,vsphere_comment):
#    #get_object_or_404(klass,*args,**kwarg) Klass可以使一个Model class，一个manager
#    #暂时不明或者一个QuerySet 迭代器 **kwarg get()或者filter()支持的类型都可以
#    vm_ips = get_object_or_404(Vsphere,pk=vsphere_comment)
#    
#    except :
#        return render(request,'adddisk/machines.html',{
#            'vm_ips':vm_ips,
#            "error_message":"Not found the machine.",
#        })
#        if vm_ip:
#            return HttpResponseRedirect(reversed('adddisk:vmdetail',args=(vsphere_comment,)),context)
#        elif vm_name:
#            return HttpResponseRedirect(reversed('adddisk:vmdetail',args=(vsphere_comment,)),context)


def newvm(request,vsphere_comment):
    """
    @ param string, IDC-ID
    @ return  vim.vim.info
    """
    vm_ips = get_object_or_404(Vsphere,pk=vsphere_comment)
    host = vm_ips.vsphere_host
    user = vm_ips.vsphere_username
    pwd  = vm_ips.vsphere_password
    try:
        if request.method == "POST":
            # json 格式

            req = request.POST
            vm_name = req['vmname']
            vm_ip   = req['vmip']
            vm_ip_Confirm   = req['vmipConfirm']
            cpu     = req['Cpu']
            memory  = req['Memory']
            # Vlan    = req['Vlan']
            Template= req['Template']
            cluster_name = req['cluster']
            disk_size= req['extra_size']
            #因datacenter之后一个所以不收集
            #resource_pool因没有利用起来所以也不采集
            logging.info("集群：%s, IP: %s" %(cluster_name, vm_ip))
            if vm_ip != vm_ip_Confirm:
                raise OSError

            Vlans = vm_ip.split('.')
            if vsphere_comment == "9f":
                Vlan =  ("vlan%s") % (Vlans[2])
            else:
                Vlan = ("vlan%s") %(int(Vlans[2]) * 10)
            logging.info(Vlan)

            datastore_name = "vmsys"
            if Template == "mysqlTemplate" or Template == "oracleTemplate":
                datastore_name = "vmdb"

            if  cluster_name == "banksteel":
                cluster_name = "钢银9f"
                datastore_name = "DNAS-Pro-Banksteel"
            elif cluster_name == "mysteel":
                cluster_name = "钢联9f"
                datastore_name = "DNAS-Pro-Mysteel"
            elif not cluster_name:
                if vsphere_comment == "pbs":
                    cluster_name = "鹏博士"
                elif vsphere_comment == "hcbanksteel":
                    cluster_name = "南翔"
                elif vsphere_comment == "hcmysteel":
                    cluster_name = "钢联"

            if req['store_position_host']:
                datastore_name = req['store_position_host']
            logging.info("最终集群位置:%s,存取器位置: %s" %(cluster_name, datastore_name))

            logging.info("IDC:%s,user:%s" %(host,user))
            si = service_con(host,user,pwd)
            content = si.RetrieveContent()
            logging.info("数据中心IDC:{}".format(vm_ips.vsphere_comment))
            try:
                clone_action = CloneDelay(content,vm_name,si,cluster_name,datastore_name,
                                        Template,vm_ip,cpu,memory,Vlan,disk_size,
                                        vsphere_comment
                                        )
                # clone_action = json.load(clone_action)
            
                context = {
                    'vm_ips':vm_ips,
                    'cloneaction':clone_action,
                }
            except:
                raise 
        else:
            context = {'vm_ips':vm_ips}
        logging.info("最終的context信息為:{}".format(context))
        return render(request,'clonevm/newvm.html',context)
    except OSError:
        #import sys
        #return HttpResponse("Unexpected error:", sys.exc_info()[0])
        return HttpResponse("<p>ip不同,请重试并修改</p></br>或者IP已被占用")
    # except:
    #     return HttpResponse("Clone出错请登录vsphere查看报警")

