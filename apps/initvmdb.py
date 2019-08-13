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

from assets.intoVMdetails import InitIntoVmDetails
from vsphere_exec.get_args import get_args, service_con
    
def main():
    vsphere_comment = "9f"
    args = get_args()
    
    host = args.host
    user = args.user
    pwd = args.password
    si = service_con(host,user,pwd)
    content = si.RetrieveContent()

    InitIntoVmDetails(vsphere_comment,content)

if __name__ == "__main__":
    main()