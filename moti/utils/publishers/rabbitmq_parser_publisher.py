import pika
import json
from pathlib import Path 
from datetime import datetime

class RabbitmqParserPublisher:
	protocol = 'rabbitmq_parser'
	def __init__(self, queues, host, port, path, name, parsers):
		self.name = name
		self.queues = queues
		self.parsers = parsers
		self.path = path
		connection = pika.BlockingConnection(
			 		 pika.ConnectionParameters(host = host,
			 						           port = port))
		channel = connection.channel()
		channel.exchange_declare(exchange = name,
								 exchange_type = 'direct')
		self.channel = channel
		for queue in queues:
			print(f"{self.name}/{queue}")
			self.channel.queue_declare(queue = f"{self.name}/{queue}")
			self.channel.queue_bind(exchange = self.name,
							   		queue = f"{self.name}/{queue}",
							   		routing_key = f"{self.name}/{queue}")

	def publish_factory(self, snapshot, queue):
		print(f"GREETINGS!! PARSER {queue}")
		parser = self.parsers.decode_queue(queue)
		self.channel.basic_publish(exchange = self.name, 
								   body = parser(snapshot, self.path),
								   routing_key = f"{self.name}/{queue}")
