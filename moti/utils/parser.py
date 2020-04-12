from functools import wraps
from pathlib import Path
import importlib
import re
from inspect import isclass
import sys

class Parser:

	def __init__(self):
		# go through utils and find parsers
		self.parsers = {}
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
					self.parsers[field] = val

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

