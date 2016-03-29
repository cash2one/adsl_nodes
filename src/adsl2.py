# -*- coding:utf-8 -*-

import os


class Adsl(object):
    def connect(self):
        cmdstr = "/sbin/ifdown ppp0"
        os.system(cmdstr)

    def disconnect(self):
        cmdstr = "/sbin/ifup ppp0"
        os.system(cmdstr)

    def reconnect(self):
        self.disconnect()
        self.connect()