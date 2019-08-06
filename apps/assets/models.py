from django.db import models

from taggit.managers import TaggableManager
from fernet_fields import EncryptedCharField


class VmDetails(models.Model):
    """
    虚拟机的信息
    """
    datacenter = models.CharField(max_length=20,verbose_name="IDC机房")
    vm_name = models.CharField(max_length=100,verbose_name="虚拟机名字")
    vm_ip = models.GenericIPAddressField(verbose_name="虚拟机内网IP",
                                                protocol='ipv4',unpack_ipv4=False
                                        )
    vm_guest_username = models.CharField(max_length=10,default="root",verbose_name="虚机用户名")
    vm_password = EncryptedCharField(verbose_name="虚机密码",max_length=200)
    department = models.CharField(verbose_name="部门",max_length=200,default="系统运维部")
    # 暂未实现,这应该是个选择的字段应该有个中间表安置部门，子部门
    vm_datastore = models.CharField(verbose_name="数据存储",max_length=50)
    vm_guest_os_name = models.CharField(verbose_name="操作系统",max_length=200)
    vm_cpu = models.IntegerField(verbose_name="CPU核数",default=4)
    vm_memory = models.IntegerField(verbose_name="内存",default=4)
    disk_size = models.IntegerField(verbose_name="总硬盘大小",default=80)
    vm_tools = models.CharField(verbose_name="VMTOOLS是否运行",max_length=30)
    powerstate = models.CharField(verbose_name="电源状态",max_length=15)
    NICstate = models.CharField(verbose_name="网卡状态",max_length=10,default="连接")
    vm_instance_UUID = models.CharField(verbose_name="UUID",max_length=200)
    create_date = models.DateField(verbose_name="创建日期",auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return self.vm_name