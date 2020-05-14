import pika
class RabbitmqConsumer:
    protocol = 'rabbitmq'
    def __init__(self, host, port, exchange_name):
        connection = pika.BlockingConnection(
                     pika.ConnectionParameters(host = host,
                                               port = port))
        channel = connection.channel()
        self.channel = channel
        self.exchange_name = exchange_name

    def add_queue(self, queue, callback):
        print(queue, callback)
        self.channel.queue_declare(queue = f"{self.exchange_name}/{queue}")
        self.channel.basic_consume(queue = f"{self.exchange_name}/{queue}",
                                   on_message_callback = callback, 
                                   auto_ack = True)

    def consume(self):
        self.channel.start_consuming()