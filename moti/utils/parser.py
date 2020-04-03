from functools import wraps
class Parser:

	def __init__(self):
		self.parsers = {}

	def wrap(self, field):
		def decorator(f):
			self.parsers[field] = f
			@wraps(f)
			def wrapper(*args, **kwargs):
				return f(*args, **kwargs)
			return wrapper
		return decorator

	def parse(self, fields, snapshot, path):
		for field in fields:
			self.parsers[field](snapshot, path)

