from furl import furl

class Consumer:
	def __init__(self, mq_url, queues, callback = None, callback_creator = None):
		queue = furl
