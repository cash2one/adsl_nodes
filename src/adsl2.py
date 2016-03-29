# -*- coding:utf-8 -*-

import os, time


class Adsl(object):
    def connect(self):
        cmdstr = "/sbin/pppoe-start"
        os.system(cmdstr)
        time.sleep(10)

    def disconnect(self):
        cmdstr = "/sbin/pppoe-stop"
        os.system(cmdstr)
        time.sleep(5)

    def reconnect(self):
        self.disconnect()
        self.connect()