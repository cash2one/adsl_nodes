# -*- coding:utf-8 -*-

from flask import Flask, request
import socket, fcntl, struct, urllib
from adsl import Adsl

app = Flask(__name__)

SERVER_URL = "http://192.168.27.37:8000/adsl"

def get_local_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret


@app.route('/', methods=['POST'])
def index():
    line = socket.gethostname()
    if request.form['dail']:
        adsl = Adsl('p4p1')
        adsl.reconnect()

        ip_adsl = get_local_ip('p4p1')
        data = urllib.urlencode({'line':line, 'ip_adsl': ip_adsl})
        ret = urllib.urlopen(SERVER_URL, data=data).read()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)








if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)