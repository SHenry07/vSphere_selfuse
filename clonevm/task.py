#Create your tasks here
# from __future__ import absolute_import, unicode_literals
# from celery import shared_task

from vsphere_exec.clone_vm import clone_vm

import os

import threading

class CloneVm(threading.Thread):
	"""clonevm"""
	def __init__(self,content,vm_name,si,cluster_name,datastore_name,Template,
	       vm_ip,cpu,memory,Vlan,disk_size):
		self.content = content
		self.vm_name = vm_name
		self.si = si
		self.cluster_name = cluster_name
		self.datastore_name = datastore_name
		self.Template = Template
		self.vm_ip = vm_ip
		self.cpu = cpu
		self.memory = memory
		self.Vlan = Vlan
		self.disk_size = disk_size
		threading.Thread.__init__(self)

	def run(self):
		clone_vm(self.content,self.vm_name,self.si,self.cluster_name,self.datastore_name,
                self.Template,self.vm_ip,self.cpu,self.memory,self.Vlan,self.disk_size
                                        )

# @shared_task
def CloneDelay(content,vm_name,si,cluster_name,datastore_name,Template,
	       vm_ip,cpu,memory,Vlan,disk_size):
	resqonse = os.system("ping  " + vm_ip)
	if resqonse == 0:
		raise OSError

	try:
		CloneVmTask = CloneVm(content,vm_name,si,cluster_name,datastore_name,Template,
	  vm_ip,cpu,memory,Vlan,disk_size)
		CloneVmTask.start()
	except:
		raise
	return CloneVmTask.is_alive()
