#!/usr/bin/python
# name  ping.py
#  ping 
#coding:utf-8

import os

def Ping_test(host):
        response = os.system("ping  " + host)

        if response == 0:
                # print( host, "is up!")
                return False
        else:
                # print (host, "is down!")
                return True


if __name__ == "__main__":
    Ping_test("192.168.100.144")