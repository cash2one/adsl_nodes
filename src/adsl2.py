# -*- coding:utf-8 -*-

import os


class Adsl(object):
    def connect(self):
        cmdstr = "/sbin/pppoe-start"
        os.system(cmdstr)

    def disconnect(self):
        cmdstr = "/sbin/pppoe-stop"
        os.system(cmdstr)

    def reconnect(self):
        self.disconnect()
        self.connect()