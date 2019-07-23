#!/usr/bin/python
# name  ping.py
#  ping 
#coding:utf-8

import os

def Ping_test(host):
        response = os.system("ping -c 3 " + host)

        if response == 0:
                print( host, "is up!")
                return False
        else:
                print (host, "is down!")
                return True


