'''
@Description: 
@Author: Henry Sun
@Date: 2019-08-07 14:11:06
@LastEditors: Henry Sun
@LastEditTime: 2019-08-14 21:53:33
'''
from django.db import models

# Create your models here.

class Vsphere(models.Model):
    """
    机房的选择
    """
    vsphere_host = models.GenericIPAddressField(verbose_name="机房vcenter的ip地址",
                                                protocol='ipv4',unpack_ipv4=False
                                                )
    vsphere_username = models.CharField(max_length=50)
    vsphere_password = models.CharField(max_length=50)
    vsphere_comment = models.CharField(max_length=20,default='9f',primary_key=True)

    idc_address = models.CharField(verbose_name="机房地址",null=True, blank=True, max_length=200)
    idc_contact = models.CharField(verbose_name="机房联系人",null=True, blank=True, max_length=50)
    idc_phone   = models.CharField(verbose_name="机房紧急电话",null=True, blank=True, max_length=50)

    class Meta:
        verbose_name = "IDC机房详细信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.vsphere_comment

