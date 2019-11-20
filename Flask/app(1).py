import socket
import sys
import os
import platform

from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    try:
        python_ver = sys.version
        osname = os.name
        platos = platform.system()
        relos = platform.release()
        kernal = platform.version()
        stname = "PISOS"
        host_name = socket.gethostname()
        flask_server_version = flask.__version__
        host_ip = socket.gethostbyname(host_name)
        now = datetime.datetime.now()
        envos = os.environ['HOME']

        return render_template('index.html', hostname=host_name, ip=host_ip, pyv=python_ver, ro=relos, on=osname,
                               po=platos, k=kernal, sn=stname, fsv=flask_server_version, dtz=now, env=envos)
    except:
        return render_template('error.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
