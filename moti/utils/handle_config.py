import yaml
from pathlib import Path
class Config_handler:
	def __init__(self, path, part = None):
		utils = Path(__file__).parent.absolute()
		path = utils / 'config/' / path
		with open(path) as reader:
			config = yaml.full_load(reader)
		if part:
			self.__dict__.update(config[part])
		else:
			self.__dict__.update(config)