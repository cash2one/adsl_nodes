# -*- coding:utf-8 -*-

import os


class Adsl(object):
    def connect(self):
        try:
            cmdstr = "/sbin/ifdown ppp0"
            os.system(cmdstr)
        except Exception:
            pass

    def disconnect(self):
        try:
            cmdstr = "/sbin/ifup ppp0"
            os.system(cmdstr)
        except Exception:
            pass

    def reconnect(self):
        self.disconnect()
        self.connect()