#Create your tasks here
from __future__ import absolute_import, unicode_literals
# from celery import shared_task
import os
import threading
import time
import logging ; logging.basicConfig(level=logging.INFO)

from assets.intoVMdetails import IntoVmDetails
from vsphere_exec.clone_vm import clone_vm, CloneError
from vsphere_exec.get_args import Get_Vm
from vsphere_exec.virtual_machine_device_info import Device_Info


class CloneVm(threading.Thread):
	"""clonevm"""
	def __init__(self,content,vm_name,si,cluster_name,datastore_name,Template,
	       vm_ip,cpu,memory,Vlan,disk_size,vsphere_comment,vm_passwd):
		self.content = content
		self.vm_name = vm_name
		self.si = si
		self.cluster_name = cluster_name
		self.datastore_name = datastore_name
		self.Template = Template
		self.vm_ip = vm_ip
		self.vm_passwd = vm_passwd
		self.cpu = cpu
		self.memory = memory
		self.Vlan = Vlan
		self.disk_size = disk_size
		self.vsphere_comment = vsphere_comment
		threading.Thread.__init__(self)

	def run(self):
		try:
			clone_vm(self.content,self.vm_name,self.si,self.cluster_name,self.datastore_name,
                self.Template,self.vm_ip,self.cpu,self.memory,self.Vlan,self.disk_size
				)
			time.sleep(30)
			vm_name = "%s(%s)" %(self.vm_name[3:],self.vm_ip)
			vm = Get_Vm(self.si,vm_name=vm_name)
			if type(vm) == str:
				raise TypeError
			result  = Device_Info(vm)
			instance_UUID = result[0]["instance UUID"]
			powerstate = result[0]['powerstate']

			disk_size = 0
			for size in result[1].values():
				# Pargm'Hard disk 1': '56,623,104 KB' 分割拼接字符串
				a = ""
				for value in size[:-3].split(','):
					a = a + value
				disk_size += int(a) /1024/1024
			IntoVmDetails(self.vsphere_comment,self.vm_name,self.vm_ip,self.vm_passwd,disk_size,instance_UUID,
					self.Template,self.cpu,self.memory,self.datastore_name,powerstate)
		except CloneError as e:
			logging.warning("克隆出错 {}".format(e))


def CloneDelay(content,vm_name,si,cluster_name,datastore_name,Template,
	       vm_ip,cpu,memory,Vlan,disk_size,vsphere_comment):
	resqonse = os.system("ping  -c 2 " + vm_ip)
	if resqonse == 0:
		raise OSError

	try:
		vm_passwd = "mysteel"
		CloneVmTask = CloneVm(content,vm_name,si,cluster_name,datastore_name,Template,
	  						vm_ip,cpu,memory,Vlan,disk_size,vsphere_comment,vm_passwd)
		CloneVmTask.start()
	
	except:
		raise
	return CloneVmTask.is_alive()
