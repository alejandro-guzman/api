import os
import socket
import subprocess

from flask import Flask, jsonify
import redis


app = Flask(__name__)

redis_host = os.environ['REDIS_HOST']
red = redis.StrictRedis(host=redis_host, port=6379, db=0)
# r.set('foo', 'bar')


@app.route("/ping")
def ping():
    uptime = subprocess.call(['cat', '/proc/uptime'])
    return jsonify({
        'hostname': socket.gethostname(),
        'uptime': uptime,
        'redis.foo': red.get('foo').decode('utf-8')
    })


app.run(host='0.0.0.0', port=5000, debug=True)
