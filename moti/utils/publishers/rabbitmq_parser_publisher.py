import pika
import json
from pathlib import Path 
from datetime import datetime

class RabbitmqParserPublisher:
	protocol = 'rabbitmq_consumer'
	def __init__(self, parsers, host, port, path, name):
		self.name = name
		self.parsers = parsers
		connection = pika.BlockingConnection(
			 		 pika.ConnectionParameters(host = host,
			 						           port = port))
		channel = connection.channel()
		channel.exchange_declare(exchange = name,
								 exchange_type = 'direct')
		self.channel = channel
		for parser in parsers:
			self.channel.queue_declare(queue = parser + self.name)
			self.channel.queue_bind(exchange = self.name,
							   		queue = parser + self.name,
							   		routing_key = parser  + self.name)
	def publish_factory(self, snapshot, parser):
		print(parser.__name__ + self.name)
		self.channel.basic_publish(exchange = self.name, 
								   body = snapshot,
								   routing_key = parser.__name__  + self.name)
