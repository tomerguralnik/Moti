from furl import furl
from .consumer import Consumer

class Transfer:
	def __init__(self, input_url, queues, publish_factory = None, publish = None):
		self.consumer = Consumer(input_url)
		self.publish_factory = publish_factory
		for queue in queues:
			if publish:
				self.consumer.add_queue(queue, publish)
			elif publish_factory:
				self.consumer.add_queue(queue, self.callback_factory(queue))
			else:
				Warning("No publishing method")

	def start(self):
		self.consumer.consume()

	def callback_factory(self, queue):
		def callback(ch, method, props, body):
			self.publish_factory(body, queue)
		return callback