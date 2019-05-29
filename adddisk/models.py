from django.db import models

# Create your models here.
class Vsphere(models.Model):
    """
    机房的选择
    """
    vsphere_host = models.GenericIPAddressField(verbose_name="机房vcenter的地址",
                                                protocol='ipv4',unpack_ipv4=False
                                                )
    vsphere_username = models.CharField(max_length=50)
    vsphere_password = models.CharField(max_length=50)
    vsphere_comment = models.CharField(max_length=20,default='9f',primary_key=True)

    def __str__(self):
        return self.vsphere_comment

    def which_host(self):
        return self.vsphere_host

class VmDetails(models.Model):
    """
    虚拟机的信息
    """

    datacenter = models.ForeignKey(Vsphere,on_delete=models.CASCADE)
    vm_name = models.CharField(max_length=200)
    vm_instance_UUID = models.CharField(max_length=200)
    vm_bios_UUID = models.CharField(max_length=200)
    vm_path_to_vm = models.CharField(max_length=200)
    vm_guest_os_name = models.CharField(max_length=100)

    def __str__(self):
        return self.vm_name

class Disk(models.Model):
    disk_size = models.IntegerField(default=0)
    disk_type = models.CharField(max_length=20,default='thin')

    def __str__(self):
        return self.disk_type

