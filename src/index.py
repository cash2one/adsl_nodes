# -*- coding:utf-8 -*-

import fcntl
import os
import socket
import struct
import urllib
import logging
import time

from flask import Flask, request, abort
from adsl2 import Adsl


LOG_FILE = '/ROOT/logs/nodes/node.log'
SERVER_URL = "http://adsl2.proxy.op.dajie-inc.com/adsl"
LOCAL_PORT = 8000

if not os.path.exists(os.path.dirname(LOG_FILE)):
    os.makedirs(os.path.dirname(LOG_FILE))

FILE_HANDLE = logging.FileHandler(LOG_FILE)
FILE_HANDLE.setLevel(logging.INFO)

app = Flask(__name__)
app.logger.addHandler(FILE_HANDLE)


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


def reloadservice(tinyproxy):
    cmdstr = "service " + tinyproxy + " reload"
    os.system(cmdstr)


def isopen(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def killprocessbyport(port):
    cmdstr = 'kill `lsof -i:' + str(port) + ' -t`'
    os.system(cmdstr)


@app.route('/', methods=['POST'])
def index():
    line = socket.gethostname()
    if request.form['dail']:
        adsl = Adsl()
        adsl.reconnect()

        ip_adsl = get_local_ip('ppp0')
        ip_idc = get_local_ip('eth0')

        tm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        msg = tm + '\t' + line + ' re-dail successfully! new ip is ' + ip_adsl
        app.logger.info(msg=msg)

        changeupstream(ip_adsl)
        reloadservice("tinyproxy")

        data = urllib.urlencode({'line': line, 'ip_idc': ip_idc, 'ip_adsl': ip_adsl, 'status': 'new'})
        ret = urllib.urlopen(SERVER_URL, data=data).read()

        return ret
    else:
        abort(404)


if __name__ == '__main__':
    ip_idc = get_local_ip('eth0')

    # print '3'
    # if isopen(ip_idc, LOCAL_PORT):
    #     killprocessbyport(LOCAL_PORT)
    # print '4'
    app.run(host=ip_idc, port=LOCAL_PORT, debug=True)
