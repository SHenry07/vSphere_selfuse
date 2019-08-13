from __future__ import absolute_import
import re
import logging
from pyVmomi import vim 
from django.db.utils import DataError
from django.core.exceptions import ObjectDoesNotExist

# import sys
# sys.path.append('../')

from vsphere_exec.get_args import service_con
from vsphere_exec.virtual_machine_device_info import Device_Info
from apps.Logout import Logger
from .models import VmDetails
from elementryinfo.models import Vsphere 


log = Logger('logs/warning.log',level='warning')

def IntoVmDetails(vsphere_comment,vm_name,vm_ip,vm_passwd,disk_size,instance_UUID,
                Template,cpu,memory,datastore,powerstate):
    try:
        #判断主机是否已写入数据库
        VmDetails.objects.get(vm_instance_UUID = instance_UUID)
        Logger('logs/error.log', level='error').logger.error('主机已存在')
    except ObjectDoesNotExist:
        data = VmDetails()
        data.datacenter = vsphere_comment
        data.vm_name = vm_name
        data.vm_ip = vm_ip
        data.vm_password = vm_passwd
        data.vm_datastore =  datastore
        data.vm_cpu = int(cpu)
        data.vm_memory = int(memory)
        data.disk_size = disk_size
        data.vm_guest_os_name = Template[:-8]
        data.vm_instance_UUID = instance_UUID
        data.powerstate = powerstate
        data.vm_tools = "guestToolsRunning"
        data.NICstate = "连接"
        data.save()
        data.tags.add("saltstack","zabbix")
        data.save()

def CronUpdateVMdetails():
    '''
    @description:更新虚机信息 
    如果新数据有，但原数据没有，则新增；
    如果新数据没有，但原数据有，则删除原来多余的部分；
    如果新的和原数据都有，则更新。
    使用集合数据类型中差的概念，处理不同的情况。
    @param {instance_UUID}
    @return: 无
    密码功能没有添加 vmtools判断问题
    string vim要求的管理类型详见APIcontent = si.RetrieveContent()
    '''    
    # for idc in Vsphere.objects.all():
    for idc in Vsphere.objects.filter(vsphere_comment='9f'):
        host = idc.vsphere_host
        user = idc.vsphere_username
        pwd  = idc.vsphere_password
        vsphere_comment = idc.vsphere_comment
        si = service_con(host,user,pwd)
        content = si.RetrieveContent()
        vms = vsphere(content)
        for vm in vms:
            result = Device_Info(vm)
            if result[0]['Template']:
                continue
            instance_UUID = result[0]['instance UUID']
            try:
            #判断主机是否已写入数据库
                old_onevm = VmDetails.objects.filter(vm_instance_UUID = instance_UUID)
                if old_onevm:
                    searchObj = re.search(r'(.*)\((.*?)\).*', result[0]['name'])
                    if searchObj:
                        vm_name = searchObj.group(1)
                        vm_ip = searchObj.group(2)
                    else:
                        log.logger.warning('命名不规范: {} {}'.format(result[0]['name'],vsphere_comment))
                        continue

                    datastore = re.search(r'\[(.*?)\].*',result[0]['path to VM'])
                    vm_datastore = datastore.group(1) 
                    if not result[0]['Cpu']:
                        log.logger.warning('主机处于不可连接状态: {} {}'.format(result[0]['name'],vsphere_comment))
                        continue

                    vm_cpu = int(result[0]['Cpu'])
                    vm_memory = int(result[0]['memory Size'])/1024
            
                    disk_size = 0
                    for size in result[1].values():
                    # Pargm'Hard disk 1': '56,623,104 KB' 分割拼接字符串
                        a = ""
                        for value in size[:-3].split(','):
                            a = a + value
                        disk_size += int(a) /1024/1024

                    vm_tools = result[0]["vmtools"]
                    powerstate = result[0]['powerstate']
                    NICstate = "关闭"
                    if powerstate == "poweredOn":
                        for nic in result[2].values():
                            connnectstate = nic[0]
                            if not connnectstate:
                                NICstate = "未启用"
                            else:
                                NICstate = "连接"
                    logging.info("name: %s 电源状态 %s 网卡状态: %s" % (result[0]['name'],powerstate,
                                                                NICstate))       

                    old_onevm.update(vm_name=vm_name,vm_ip=vm_ip,vm_cpu=vm_cpu,vm_memory=vm_memory,
                                    vm_tools=vm_tools,powerstate=powerstate,NICstate=NICstate,disk_size=disk_size,
                                    vm_datastore=vm_datastore)
                    print("更新成功")
                else:
                    data = VmDetails()
                    data.datacenter = vsphere_comment

                    searchObj = re.search(r'(.*)\((.*?)\).*', result[0]['name'])
                    data.vm_name = ""
                    data.vm_ip = None
                    if searchObj:
                        data.vm_name = searchObj.group(1)
                        data.vm_ip = searchObj.group(2)
                    else:
                        log.logger.warning('命名不规范: {} {}'.format(result[0]['name'],vsphere_comment))
                        continue

                    data.vm_password = "mysteel"
                    datastore = re.search(r'\[(.*?)\].*',result[0]['path to VM'])
                    data.vm_datastore = datastore.group(1) 
                    if not result[0]['Cpu']:
                        log.logger.warning('主机处于不可连接状态: {} {}'.format(result[0]['name'],vsphere_comment))
                        continue

                    data.vm_cpu = int(result[0]['Cpu'])
                    data.vm_memory = int(result[0]['memory Size'])/1024
                
                    disk_size = 0
                    for size in result[1].values():
                    # Pargm'Hard disk 1': '56,623,104 KB' 分割拼接字符串
                        a = ""
                        for value in size[:-3].split(','):
                            a = a + value
                        disk_size += int(a) /1024/1024
                    data.disk_size = disk_size

                    data.vm_tools = result[0]["vmtools"]
                    data.powerstate = result[0]['powerstate']
                    data.vm_guest_os_name = result[0]['guest OS name']
                    data.vm_instance_UUID = result[0]['instance UUID']
                    data.NICstate = "关闭"
                    if data.powerstate == "poweredOn":
                        for nic in result[2].values():
                            connnectstate = nic[0]
                            if not connnectstate:
                                data.NICstate = "未启用"
                            else:
                                data.NICstate = "连接"
                    logging.info("name: %s 电源状态 %s 网卡状态: %s" % (result[0]['name'],data.powerstate,
                                                                    data.NICstate))       

                    data.save()
                    if vsphere_comment != "9f":
                        data.tags.add("zabbix","saltstack")
                        data.save()

            except TypeError as e:
                logging.warning('主机处于无法连接状态: {}'.format(e))
            except DataError as e:
                log.logger.warning('命名不规范: {}'.format(e))
            # except ObjectDoesNotExist:
                # Logger('logs/error.log', level='error').logger.error('主机不存在')
            



def vsphere(content):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vms = [vm for vm in vm_view.view]
    vm_view.Destroy()
    return vms