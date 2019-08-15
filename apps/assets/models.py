'''
@Description: 
@Author: Henry Sun
@Date: 2019-08-07 14:11:06
@LastEditors: Henry Sun
@LastEditTime: 2019-08-14 16:50:12
'''
from django.db import models

from taggit.managers import TaggableManager
from fernet_fields import EncryptedCharField


class VmDetails(models.Model):
    """
    虚拟机的信息
    """
    NICSTATE_CHOICE = (
        ('Unused',"未启用"),
        ('On',"连接"),
        ('Off',"关闭")
    )
    POWERSTATE_CHOICE = (
        ('On',"连接"),
        ('Off',"关闭")
    )
    VMTOOLSSTATE_CHOICE = (
        ('On',"连接"),
        ('Off',"关闭")
    )
    datacenter = models.CharField(max_length=20,verbose_name="IDC机房")
    vm_name = models.CharField(max_length=100,verbose_name="虚拟机名字")
    vm_ip = models.GenericIPAddressField(verbose_name="虚拟机内网IP",
                                                protocol='ipv4',unpack_ipv4=False
                                        )
    vm_guest_username = models.CharField(max_length=10,default="root",verbose_name="虚机用户名")
    vm_password = EncryptedCharField(verbose_name="虚机密码",max_length=200)
    department = models.CharField(verbose_name="部门",max_length=200,default="系统运维部")
    # 暂未实现,这应该是个选择的字段应该有个中间表安置部门，子部门-直接以组为概念
    vm_datastore = models.CharField(verbose_name="数据存储",max_length=50)
    vm_guest_os_name = models.CharField(verbose_name="操作系统",max_length=200)
    vm_cpu = models.IntegerField(verbose_name="CPU核数",default=4)
    vm_memory = models.IntegerField(verbose_name="内存",default=4)
    disk_size = models.IntegerField(verbose_name="总硬盘大小",default=80)
    vm_tools = models.CharField(verbose_name="VMTOOLS是否运行",choices=VMTOOLSSTATE_CHOICE,max_length=30)
    powerstate = models.CharField(verbose_name="电源状态", choices=POWERSTATE_CHOICE,max_length=15)
    NICstate = models.CharField(verbose_name="网卡状态",choices=NICSTATE_CHOICE, max_length=10,)
    vm_instance_UUID = models.CharField(verbose_name="UUID",max_length=100)
    asset_type = models.CharField(verbose_name="类型",max_length=20,default="虚拟机")
    c_time = models.DateField(verbose_name="创建日期",auto_now_add=True)
    m_time = models.DateField(verbose_name="更新日期",auto_now=True)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = "虚拟机详细信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s %s" % (self.vm_name, self.vm_ip)

