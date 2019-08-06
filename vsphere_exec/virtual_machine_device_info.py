#!/usr/bin/env python
from pyVmomi import vim
from apps.Logout import Logger

log = Logger('logs/info.log',level='info')


def Device_Info(vm):
    #"获取IP未做 vmtool判定有问题"
    details = {'name': vm.summary.config.name,
            'instance UUID': vm.summary.config.instanceUuid,
            #'bios UUID': vm.summary.config.uuid,
            #'datastore': vm.summary.vm.datastore,
            # 'datastore': Datastore.summary.name,
            'Cpu': vm.summary.config.numCpu,
            'memory Size': vm.summary.config.memorySizeMB,
            'path to VM': vm.summary.config.vmPathName,
          #  'guest OS id': vm.summary.config.guestId,
            'guest OS name': vm.summary.config.guestFullName,
            'Template': vm.summary.config.template,
           # 'host name': vm.runtime.host.name,
            'powerstate': vm.runtime.powerState,
            'vmtools': vm.summary.guest.toolsRunningStatus,
            'ipaddress': vm.summary.guest.ipAddress,
            'hostname': vm.summary.guest.hostName,
            'last booted timestamp': vm.runtime.bootTime}
    log.logger.info("被检查的虚机:{}".format(details))

    DiskInfo, NetadapterInfo = {}, {}

    for device in vm.config.hardware.device:
        # diving into each device, we pull out a few interesting bits
        if isinstance(device, vim.vm.device.VirtualDisk):
            # dev_details = {#'key': device.key,
            #         'lable' : device.deviceInfo.label,
            #         'summary': device.deviceInfo.summary,
                    # 'whetherconnected': device.connectable,
           #         'device type': type(device).__name__,
           #         'backing type': type(device.backing).__name__
                    # }
            DiskInfo[device.deviceInfo.label] = device.deviceInfo.summary
        if isinstance(device, vim.vm.device.VirtualEthernetCard):
            label = device.deviceInfo.label
            NetadapterInfo[label] = device.connectable.connected, device.connectable.status
                                                          

        #print(u"  label: {0}".format(device.deviceInfo.label))
        #print(u"  ------------------")
    # for name, value in DiskAndNet_adapter.items():
        # print(name,value)
    return details,DiskInfo,NetadapterInfo
    