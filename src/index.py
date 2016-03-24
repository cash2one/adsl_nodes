# -*- coding:utf-8 -*-

import fcntl
import os
import socket
import struct
import urllib

from flask import Flask, request

from adsl2 import Adsl

app = Flask(__name__)

SERVER_URL = "http://192.168.27.37:8000/adsl"


def get_local_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret


def changeupstream(ip_ppp):
    with open("tinyproxy.conf") as f:
        content = f.read()

    newcontent = content.replace("IP_PPP", ip_ppp)
    with open("/etc/tinyproxy/tinyproxy.conf", 'w') as f:
        f.write(newcontent)


def reloadtinyproxy(tinyproxy):
    cmdstr = "service " + tinyproxy + " reload"
    os.system(cmdstr)


@app.route('/', methods=['POST'])
def index():
    line = socket.gethostname()
    if request.form['dail']:
        adsl = Adsl()
        adsl.reconnect()

        ip_adsl = get_local_ip('ppp0')
        changeupstream(ip_adsl)
        reloadtinyproxy("tinyproxy")

        data = urllib.urlencode({'line': line, 'ip_adsl': ip_adsl})
        ret = urllib.urlopen(SERVER_URL, data=data).read()

        print ret


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
