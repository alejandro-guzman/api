import json
from logging.config import dictConfig
import os
import socket
import subprocess
import time

from flask import Flask, jsonify
from redis import StrictRedis
from pika import BlockingConnection, ConnectionParameters
from pymongo import MongoClient


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)

redis_host = os.environ['REDIS_HOST']
redis_port = int(os.environ['REDIS_PORT'])
red_client = StrictRedis(host=redis_host, port=redis_port, db=0)

rabbitmq_host = os.environ['RABBITMQ_HOST']
rabbitmq_conn = BlockingConnection(ConnectionParameters(host=rabbitmq_host))
rmq_channel = rabbitmq_conn.channel()
rmq_channel.queue_declare(queue='job')

mongo_host = os.environ['MONGO_HOST']
mongo_port = int(os.environ['MONGO_PORT'])
mongo_conn = MongoClient(host=mongo_host, port=mongo_port)


@app.route('/produce/<message>')
def produce(message):
    # Create message
    body = json.dumps({
        'created': time.ctime(),
        'message': message
    })

    try:
        app.logger.info('Trying to publish message: {}'.format(body))
        rmq_channel.basic_publish(exchange='', routing_key='job', body=body)
        resp = dict(result='OK')
    except Exception as e:
        app.logger.exception('Exception publishing message: {}'.format(body))
        resp = dict(result='ERR', details=str(e))

    return jsonify(resp)

@app.route('/set/<key>/<value>')
def _set(key, value):
    app.logger.exception('Trying to set {} to {} '.format(key, value))
    red_client.set(key, value)
    return jsonify({
        'result': 'OKAY'
    })

@app.route('/get/<key>')
def get(key):
    return jsonify({
        key: red_client.get(key).decode('utf-8')
    })

@app.route("/ping")
def ping():
    print('hello')
    return jsonify(dict(hostname=socket.gethostname(),
                        uptime=subprocess.call(['cat', '/proc/uptime'])))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
