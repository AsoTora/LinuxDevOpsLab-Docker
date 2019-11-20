import flask
import socket
import sys
import os
import platform
import tzlocal

from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)
day = datetime.strptime(time, "%Y-%m-%d_%H:%M:%S")

@app.route("/")
def index():
    try:
        python_ver = sys.version
        osname = os.name
        platos = platform.system()
        relos = platform.release()
        kernal = platform.version()
        stname = "Yauheni_Matveichyk"
        host_name = socket.gethostname()
        flask_server_version = flask.__version__
        host_ip = socket.gethostbyname(host_name)
        now = datetime.now(tzlocal.get_localzone())  # python 3 import time && time.localtime().tm_zone
        envos = os.environ['HOME']
        build_time = day.strftime('%H:%M:%S / %d.%m.%Y')

        return render_template('index.html', hostname=host_name, ip=host_ip, pyv=python_ver, ro=relos, on=osname,
                               po=platos, k=kernal, sn=stname, fsv=flask_server_version, dtz=now, env=envos, 
                               bt=build_time)
    except:
        return render_template('error.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
