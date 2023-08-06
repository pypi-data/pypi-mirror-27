from .base import Base
import pika
import json


class Publish(Base):
    
    def publish(self, exchange, routing_key, body, type='fanout', durable=False):
        self.channel.exchange_declare(exchange=exchange, exchange_type=type, durable=durable)
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(body)
        )
        self.connection.close()
