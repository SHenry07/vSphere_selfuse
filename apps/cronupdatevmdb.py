from __future__ import absolute_import, unicode_literals

import sys 
import os
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../"+"../")
# 设置文件路径变量，导入django设置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmdb.settings")
# from virtual_machine_device_info import Device_Info
import django
django.setup()

from assets.intoVMdetails import CronUpdateVMdetails
    
def main():
    CronUpdateVMdetails()
 

if __name__ == "__main__":
    main()