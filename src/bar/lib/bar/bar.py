import logging
import os
import sys

from pika import BlockingConnection, ConnectionParameters
from pymongo import MongoClient


rabbitmq_host = os.environ['RABBITMQ_HOST']
rabbitmq_conn = BlockingConnection(ConnectionParameters(host=rabbitmq_host))
rmq_channel = rabbitmq_conn.channel()
rmq_channel.queue_declare(queue='job')

client = MongoClient('db')

log = logging.getLogger(__name__)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
stdout_handler.setLevel(logging.DEBUG)
log.addHandler(stdout_handler)
log.setLevel(logging.DEBUG)


def handler(ch, method, properties, body):
    client.demo.bodies.insert({'body': body})
    log.warning('got something: %s' % body)

if __name__ == '__main__':
    rmq_channel.basic_consume(handler, queue='job', no_ack=False)
    log.info('[*] Waiting for messages. To exit press CTRL+C')
    rmq_channel.start_consuming()
