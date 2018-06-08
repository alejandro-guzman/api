import subprocess
import socket
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/ping")
def ping():
    uptime = subprocess.call(['cat', '/proc/uptime'])
    return jsonify({
        'hostname': socket.gethostname(),
        'uptime': uptime
    })


app.run(host='0.0.0.0', port=5000, debug=True)
