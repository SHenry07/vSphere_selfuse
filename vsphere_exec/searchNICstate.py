# from __future__ import absolute_import
import re
import logging
from pyVmomi import vim 
import sys
import os

from virtual_machine_device_info import Device_Info
from get_args import get_args, service_con

def SearchVmDetails(content):
    """
    @description:查询网卡非启用主机
    @param {type} string vim要求的管理类型详见APIcontent = si.RetrieveContent()
    @return: 无
    """
    vm_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vms = [vm for vm in vm_view.view]
    vm_view.Destroy()
    for vm in vms:
        try:
            result = Device_Info(vm)

            if result[0]['Template']:
                continue
            print(result)

            vm_tools = result[0]["vmtools"]
            powerstate = result[0]['powerstate']

            NICstate = "连接"
            if powerstate == "poweredOn":
                for lable, nic in result[2].items():
                    connnected = nic[0]
                    status     = nic[1]
                    if not connnected and status == 'ok':
                        NICstate = "未启用"
                        logging.info("name: %s 电源状态 %s 网卡名: %s 状态: %s vmtools状态: %r" 
                        % (result[0]['name'],powerstate,lable,NICstate,vm_tools))
            else:
                NICstate = "关闭"
            # logging.info("name: %s 电源状态 %s 网卡状态: %s vmtools状态: %r" 
                        # % (result[0]['name'],powerstate,NICstate,vm_tools))

            # print(datacenter,vm_name,vm_ip,vm_password,vm_datastore,vm_cpu,vm_memory,type(vm_tools),
            # powerstate,vm_guest_os_name,vm_instance_UUID,NICstate)
        except TypeError as e:
            logging.warning('主机无法连接: {}'.format(e))
    

if __name__ == "__main__":

    args = get_args()
    
    host = args.host
    user = args.user
    pwd = args.password
    si = service_con(host,user,pwd)
    content = si.RetrieveContent()

    SearchVmDetails(content)