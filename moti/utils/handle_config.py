import yaml
from pathlib import Path
class Config_handler:
	def __init__(self, path, part = None):
		"""
		Loads the desired part of config file into __dict__

		:param path: path to config file
		:type path: str
		:param part: the name of the part of the config file you want, defaults to None
		:type part: str or None(,optional)
		"""
		utils = Path(__file__).parent.absolute()
		path = utils / 'config/' / path
		with open(path) as reader:
			config = yaml.full_load(reader)
		if part:
			self.__dict__.update(config[part])
		else:
			self.__dict__.update(config)