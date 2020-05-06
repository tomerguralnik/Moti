from functools import wraps
from pathlib import Path
import importlib
import re
from inspect import isclass
import sys

class Parser:

	def __init__(self):
		# go through utils and find parsers
		self.parsers = []
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
				self.parsers.append(val)
				for field in val.__dict__['fields']:
					self.fields.append(field)
					if not field in self.mapping:
						self.mapping[field] = []
					self.mapping[field].append(val)

	def wrap(self, field):
		def decorator(f):
			self.parsers.append(f)
			self.fields.append(field)
			@wraps(f)
			def wrapper(*args, **kwargs):
				return f(*args, **kwargs)
			return wrapper
		return decorator

	def parsers_to_string(self):
		return map(lambda func: func.__name__, self.parsers)

	def parse_field(self, field, data, context):
		return [parser(data, context) for i in self.mapping[field]]

 

