#!/usr/bin/env python
"""
Written by Dann Bohn
Github: https://github.com/whereismyjetpack
Email: dannbohn@gmail.com

Clone a VM from template example
"""
from pyVmomi import vim
import atexit

#from add_nic_to_vm import add_nic
from .add_disk_to_vm import add_disk
from .getvnicinfo import GetVMNics
import logging ; logging.basicConfig(level=logging.INFO)
#import get_args

class CloneError(Exception):
    pass

def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            task_done = True
            raise CloneError("there was an error")


def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj


def clone_vm(
        content,vm_name, si,cluster_name,datastore_name, template,vm_ip,
        cpu,memory,Vlan,disk_size,
        vm_folder="暂存待分配"):
    """
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    datacenter_name数据中心名字cluster_name集群名字
    参考了nsxt_change_vm_vif.py  利用了getvicinfo.py
    """
    template = get_obj(content, [vim.VirtualMachine], template)
    # if none get the first one
    datacenter_name = None
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)

    if vm_folder:
        destfolder = get_obj(content, [vim.Folder], vm_folder)
    else:
        destfolder = datacenter.vmFolder

    if datastore_name:
       datastore = get_obj(content, [vim.Datastore], datastore_name)
    else:
       datastore = get_obj(
           content, [vim.Datastore], template.datastore[0].info.name)

    # if None, get the first one
    cluster = get_obj(content, [vim.ClusterComputeResource], cluster_name)

    resource_pool = cluster_name
    if resource_pool:
        resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
    else:
        resource_pool = cluster.resourcePool

    # Properties属性  Parameters 参数
    # 要分清API是class还是method


    # set relospec 即Vm关联配置Vm放到哪里
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    # 配置vm硬件设备
    vm_config = vim.vm.ConfigSpec()
    vm_config.numCPUs = int(cpu)  
    vm_config.memoryMB = int(memory)*1024  
    vm_config.cpuHotAddEnabled = True  
    vm_config.memoryHotAddEnabled = True


    # 添加额外的硬盘没有必要自己实现因为和add_disk一样VirtualMachine.Config.AddNewDisk

    #改变GuestHostName
    guestname = vm_name
    # hostName = vim.vm.customization.FixedName(guestname)
    identity = vim.vm.customization.LinuxPrep()
    identity.domain = "mysteel.com"
    identity.timeZone = "Asia/Shanghai"
    identity.hwClockUTC = False
    identity.hostName = vim.vm.customization.FixedName()
    identity.hostName.name = guestname

    dns = vim.vm.customization.GlobalIPSettings()
    dns.dnsSuffixList = "mysteel.com"
    dns.dnsServerList = "172.17.2.224"
    globalIPSettings = dns

    #改变GuestIP
    ip = vim.vm.customization.FixedIp()
    ip.ipAddress = vm_ip
    adapter = vim.vm.customization.IPSettings()
    adapter.ip = ip
    adapter.subnetMask = "255.255.255.0"
    adapter.gateway = "172.16.0.250"

    nicSettingMap = []
    nicSettingMap.append(vim.vm.customization.AdapterMapping())
    nicSettingMap[0].adapter = adapter
   
    
    
    GuestConfig = vim.vm.customization.Specification()
    GuestConfig.identity = identity
    GuestConfig.globalIPSettings = globalIPSettings
    GuestConfig.nicSettingMap = nicSettingMap

    # 生成自定义规则文件
    # GuestConfig_info = vim.CustomizationSpecInfo()
    # GuestConfig_info.description = "Linuxforweb"
    # GuestConfig_info.name = "linuxforscripts-web"
    # GuestConfig_info.type = "Linux"

    # scripts_item = vim.CustomizationSpecItem()
    # scripts_item.spec = GuestConfig
    # scripts_item.info = GuestConfig_info

    #print(scripts_item)
    #vm_customization_origin = content.customizationSpecManager.GetCustomizationSpec("linuxforscripts")
    #vm_customization = 
    # content.customizationSpecManager.OverwriteCustomizationSpec(scripts_item)


    # print ("初始化配置",vm_config)
    clonespec = vim.vm.CloneSpec()
    clonespec.config = vm_config
    clonespec.customization = GuestConfig
    clonespec.location = relospec
    clonespec.powerOn = False

    logging.info("克隆最终配置: {}" .format(clonespec))
    # print("cloning VM...")

    vm_name = vm_name[3:]
    vm_name = "%s(%s)" %(vm_name,vm_ip) 

    # 检查自定义规范
    # print(template.CheckCustomizationSpec(GuestConfig))

    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    wait_for_task(task)

    # 修改vlan
    nic_changes = []
    vm = get_obj(content, [vim.VirtualMachine], vm_name)
    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualEthernetCard):
            nic_spec = vim.vm.device.VirtualDeviceSpec()
            nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit

            nic_spec.device = device
            portgroup = get_obj(content,
                         [vim.dvs.DistributedVirtualPortgroup], Vlan)
    # dvs = portgroup.config.distributedVirtualSwitch
    # portKey = search_port(dvs, portgroup.key)
    # port = port_find(dvs, portKey)
        
            dvs_port_connection = vim.dvs.PortConnection()
            dvs_port_connection.portgroupKey = portgroup.key
            dvs_port_connection.switchUuid = \
                portgroup.config.distributedVirtualSwitch.uuid
            nic_spec.device.backing = \
            vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            nic_spec.device.backing.port = dvs_port_connection
            nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
            nic_spec.device.connectable.startConnected = True
            nic_spec.device.connectable.allowGuestControl = True
            nic_spec.device.connectable.connected = False
            nic_spec.device.connectable.status = 'untried'
            nic_spec.device.wakeOnLanEnabled = True
            nic_spec.device.addressType = 'assigned'

    nic_changes.append(nic_spec)
    config_spec = vim.vm.ConfigSpec(deviceChange = nic_changes)
    task_change_vlan = vm.ReconfigVM_Task(config_spec)
    wait_for_task(task_change_vlan)


    if disk_size:
        disk_size = int(disk_size)
        task_add_disk = add_disk(vm,si,disk_size) 
        task_add_disk

    task_poweron = vm.PowerOnVM_Task()
    return wait_for_task(task_poweron)





    

 
    

# def search_port(dvs, portgroupkey):
#     search_portkey = []
#     criteria = vim.dvs.PortCriteria()
#     criteria.connected = False
#     criteria.inside = True
#     criteria.portgroupKey = portgroupkey
#     ports = dvs.FetchDVPorts(criteria)
#     for port in ports:
#         search_portkey.append(port.key)
#     # print(search_portkey)
#     return search_portkey[0]


# def port_find(dvs, key):
#     obj = None
#     ports = dvs.FetchDVPorts()
#     for c in ports:
#         if c.key == key:
#             obj = c
#     return obj



