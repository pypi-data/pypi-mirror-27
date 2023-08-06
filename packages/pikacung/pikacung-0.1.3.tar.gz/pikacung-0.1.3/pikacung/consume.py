from .base import Base
import pika


class Consume(Base):

    def __init__(self, callback, host='localhost', port=5672, virtual_host='/', username='guest', password='guest'):
        super().__init__(host, port, virtual_host, username, password)
        self.callback = callback
        self.before_consuming = None
    
    def consume(self, exchange, routing_key, exclusive=True, no_ack=True, type='fanout', durable=False):
        self.channel.exchange_declare(exchange=exchange, exchange_type=type, durable=durable)

        result = self.channel.queue_declare(exclusive=exclusive)
        queue_name = result.method.queue

        self.channel.queue_bind(queue=queue_name, exchange=exchange, routing_key=routing_key)
        self.channel.basic_consume(self.callback, queue=queue_name, no_ack=no_ack)

        if not self.before_consuming is None:
            self.before_consuming()

        self.channel.start_consuming()
