from functools import wraps
from pathlib import Path
import importlib
import re
from inspect import isclass
import sys

class Parser:

	def __init__(self, fields = None):
		# go through utils and find parsers
		self.fields = []
		self.mapping = {}
		utils = Path(__file__).parent.absolute() #path to utils
		parsers = utils/'parsers'
		sys.path.insert(0, str(utils))
		for path in parsers.iterdir():
			if not (path.is_file() and path.suffix == '.py'):
				continue
			m = importlib.import_module(f'{parsers.name}.{path.stem}')
			for name in m.__dict__:
				val = m.__dict__[name]
				if not(re.match('parse_*', name) and callable(val) and 'fields' in val.__dict__.keys()):
					continue
				for field in val.__dict__['fields']:
					self.fields.append(field)
					if not field in self.mapping:
						self.mapping[field] = []
					self.mapping[field].append(val)
		if fields != None:
			for field in self.fields:
				if field in fields:
					continue
				del self.mapping[field]
			self.fields = list(filter(lambda x: x in fields, self.fields))
			

	def wrap(self, field):
		def decorator(f):
			self.fields.append(field)
			if not field in self.mapping:
				self.mapping[field] = []
			self.mapping[field].append(f)
			@wraps(f)
			def wrapper(*args, **kwargs):
				return f(*args, **kwargs)
			return wrapper
		return decorator

	def generate_queues(self):
		queues = []
		for field in self.fields:
			for i in range(len(self.mapping[field])):
				queues.append(f"{field}/{i}")
		return queues

	def decode_queue(self, queue):
		field, number = queue.split('/')
		return self.mapping[field][int(number)]

	def parse_field(self, field, data, context):
		return [parser(data, context) for i in self.mapping[field]]

 

