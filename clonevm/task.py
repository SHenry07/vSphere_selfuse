# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

import os
# from vsphere_exec.clone_vm import  clone_vm
# @shared_task
# def CloneDelay(*args,**kwargs):
# 	clone_action = clone_vm(content,vm_name,si,cluster_name,datastore_name,
#                                         Template,vm_ip,cpu,memory,Vlan,disk_size
#                                         )
# 	# return clone_action

@shared_task
def Ping_Test_Check(host,*args, **kwargs):
	reponse = os.system("ping -n 3 " + host)
	if reponse == 0:
		return False
	else:
		return True
@shared_task
def xsum(numbers):
	return sum(numbers)
