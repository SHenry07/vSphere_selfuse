#Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from vsphere_exec.clone_vm import clone_vm

import os


@shared_task
def CloneDelay(content,vm_name,si,cluster_name,datastore_name,Template,
	       vm_ip,cpu,memory,Vlan,disk_size):
	resqonse = os.system("ping -c 3 " + vm_ip)
	if resqonse == 0:
		raise OSError

	return clone_vm(content,vm_name,si,cluster_name,datastore_name,Template,
	  vm_ip,cpu,memory,Vlan,disk_size)
