import pika
import json
from pathlib import Path 
from datetime import datetime

class RabbitmqServerPublisher:
	protocol = 'rabbitmq_server'
	def __init__(self, queues, host, port, path, name):
		self.name = name
		self.path = path / 'publish_records'
		self.path.mkdir(exist_ok = True)
		self.queues = queues
		connection = pika.BlockingConnection(
			 		 pika.ConnectionParameters(host = host,
			 						           port = port))
		channel = connection.channel()
		channel.exchange_declare(exchange = name,
								 exchange_type = 'fanout')
		self.channel = channel
		for queue in queues:
			self.channel.queue_declare(queue = f"{self.name}/{queue}")
			self.channel.queue_bind(exchange = self.name,
							   		queue = f"{self.name}/{queue}")

	def publish(self, snapshot):
		msg = str(self._to_json(snapshot))
		self.channel.basic_publish(exchange = self.name, 
								   body = msg,
								   routing_key = '')

	def _to_json(self, snapshot):
		path = self.path / str(snapshot.user['user_id'])
		path.mkdir(exist_ok = True)
		path = path / (datetime.fromtimestamp(snapshot.timestamp/1000).strftime('%Y-%m-%d_%H-%M-%S.%f') + '.json')
		path.touch()
		fp = path.open('w')
		to_dump = snapshot.compactify(path.parent)
		to_dump['user'] = snapshot.user
		json.dump(to_dump, fp)
		return path.absolute()
