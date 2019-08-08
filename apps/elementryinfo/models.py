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
