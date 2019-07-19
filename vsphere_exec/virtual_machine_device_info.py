#!/usr/bin/env python
from __future__ import print_function

def Device_Info(vm):
 #   print(u"Found Virtual Machine")
 #   print(u"=====================")
    details = {'name': vm.summary.config.name,
            'instance UUID': vm.summary.config.instanceUuid,
            'bios UUID': vm.summary.config.uuid,
            'path to VM': vm.summary.config.vmPathName,
            'guest OS id': vm.summary.config.guestId,
            'guest OS name': vm.summary.config.guestFullName,
            'host name': vm.runtime.host.name,
            'last booted timestamp': vm.runtime.bootTime}

    DiskAndNet_adapter = {}

    for device in vm.config.hardware.device:
 #       print(device)
        # diving into each device, we pull out a few interesting bits

        dev_details = {#'key': device.key,
                    'lable' : device.deviceInfo.label,
                    'summary': device.deviceInfo.summary,
                    'whetherconnected': device.connectable,
                   # 'device type': type(device).__name__,
                    #'backing type': type(device.backing).__name__
                    }
        DiskAndNet_adapter[device.deviceInfo.label] = dev_details

        #print(u"  label: {0}".format(device.deviceInfo.label))
        #print(u"  ------------------")
        #for name, value in dev_details.items():
        #    print(u"    {0:{width}{base}}: {1}".format(name, value,
        #                                            width=15, base='s'))
        for name,value in DiskAndNet_adapter.items():
            print(name,value)
    return details,dev_details
    
#if __name__ == '__main__':
#    for name, value in details.items():
#        print(u"  {0:{width}{base}}: {1}".format(name, value, width=25, base='s'))
