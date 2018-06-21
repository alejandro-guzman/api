import os

from pika import BlockingConnection, ConnectionParameters


rabbitmq_host = os.environ['RABBITMQ_HOST']
rabbitmq_conn = BlockingConnection(ConnectionParameters(host=rabbitmq_host))
rmq_channel = rabbitmq_conn.channel()
rmq_channel.queue_declare(queue='job')


def handler(ch, method, properties, body):
    print(" [x] Received %r" % body)


if __name__ == '__main__':
    rmq_channel.basic_consume(handler, queue='job', no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    rmq_channel.start_consuming()
