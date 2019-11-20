import flask
import socket
import sys
import os
import platform
import datetime
import subprocess
from flask import Flask

app = Flask(__name__)
bday = datetime.datetime.now()


@app.route("/")
def myapp():
    python_ver = sys.version
    flask_ver = flask.__version__
    os_name = platform.platform()
    os_fam = platform.system()
    os_rel = platform.release()
    kernel = platform.version()
    build_date = bday
    page_date = datetime.datetime.now()
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    name = "Yury Kachatkou"
    env = os.environ['PATH']
    cmd = "ps -p 1 -o etime | awk 'FNR==2'"
    curl_file = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    cont_life = curl_file.stdout.read()

    result = "Python version: {}\nFlask Version: {}\nSystems OS Name: {}, Release Version: {}, Family Name: {}\n" \
             "Kernel Version: {}\nBuild date: {}\nPage generation date:{}\nSystem Host Name:{}, IP address:{}\n" \
             "Student Name: {}\n Environment Variable: {}\nContainer Life time:{}".format(python_ver,
                                                                  flask_ver,
                                                                  os_name,
                                                                  os_rel, os_fam, kernel, build_date, page_date,
                                                                  host_name, host_ip, name, env, cont_life)

    return result
    if __name__ == "__main__":
        myapp.run(host='0.0.0.0', port=5000)
