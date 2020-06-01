import pika
import json
from pathlib import Path 
from datetime import datetime

class RabbitmqParserPublisher:
	protocol = 'rabbitmq_parser'
	def __init__(self, queues, host, port, path, name, parsers):
		"""
		Initiate a pika connection, declare all queues and add them to
		the exchange
		all queue's names are change to {name}/{queue}
		:param queues: list of queues to declare
		:type queues: list
		:param host: ip of the message queue
		:type host: str
		:param port: port of the message queue
		:type port: int
		:param path: path to directory where parsers should save their data
		:type path: str
		:param name: name of the desired exchange
		:type name: str
		:param parsers: a Parser object containing all wanted parsers
		:tpye parsers: Parser
		"""
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
			self.channel.queue_declare(queue = f"{self.name}/{queue}")
			self.channel.queue_bind(exchange = self.name,
							   		queue = f"{self.name}/{queue}",
							   		routing_key = f"{self.name}/{queue}")

	def publish_factory(self, snapshot, queue):
		"""
		This function parses the snapshot based on the parser specified by queue 
		and sends the result to the exchange for parser publishers
		
		:param snapshot: snapshot as read from a message queue
		:type snaoshot: str, a path to a json file containing snapshot
		:param queue: name of queue the snapshot was rea from
		:type queue: str
		"""
		parser = self.parsers.decode_queue(queue)
		self.channel.basic_publish(exchange = self.name, 
								   body = parser(snapshot, self.path),
								   routing_key = f"{self.name}/{queue}")
