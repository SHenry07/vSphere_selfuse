#!/usr/bin/env python
"""
Written by Dann Bohn
Github: https://github.com/whereismyjetpack
Email: dannbohn@gmail.com

Script to add a Hard disk to an existing VM
This is for demonstration purposes only.
I did not do a whole lot of sanity checking, etc.

Known issues:
This will not add more than 15 disks to a VM
To do that the VM needs an additional scsi controller
and I have not yet worked through that
"""
from pyVmomi import vim
from pyVmomi import vmodl

def add_disk(vm,si,disk_size, disk_type='thin'):
        spec = vim.vm.ConfigSpec()
        # get all disks on a VM, set unit_number to the next available
        unit_number = 0
        for dev in vm.config.hardware.device:
            if hasattr(dev.backing, 'fileName'):
                unit_number = int(dev.unitNumber) + 1
                # unit_number 7 reserved for scsi controller
                if unit_number == 7:
                    unit_number += 1
                if unit_number >= 16:
                    return ("we don't support this many disks")
            if isinstance(dev, vim.vm.device.VirtualSCSIController):
                controller = dev
        # add disk here
        dev_changes = []
        new_disk_kb = int(disk_size) * 1024 * 1024
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = \
            vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        if disk_type == 'thin':
            disk_spec.device.backing.thinProvisioned = True
        disk_spec.device.backing.diskMode = 'persistent'
        disk_spec.device.unitNumber = unit_number
        disk_spec.device.capacityInKB = new_disk_kb
        disk_spec.device.controllerKey = controller.key
        dev_changes.append(disk_spec)
        spec.deviceChange = dev_changes
        vm.ReconfigVM_Task(spec=spec)
        return("%sGB disk added to %s" % (disk_size, vm.config.name))


