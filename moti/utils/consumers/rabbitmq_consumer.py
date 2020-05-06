import pika
class RabbitmqConsumer:
	def __init__(self, host, port):
		connection = pika.BlockingConnection(
                     pika.ConnectionParameters(host = host,
                                               port = port))
        channel = connection.channel()
        self.channel = channel

    def add_queue(self, queue, callback):
    	self.channel.queue_declare(queue = queue)
    	self.channel.basic_consume(queue = queue,
    							   on_message_callback = callback,
    							   auto_ack = True)