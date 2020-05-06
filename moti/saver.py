from furl import furl
from pathlib import Path
import importlib
from .cli import saver_cli
from .utils import Consumer

@saver_cli.command()
@click.option('--database', '-d', help = 'Database url')
@click.option('--field', '-f', help = 'Field')
@click.option('--data', help = 'data')
def save(database, field, data):
	saver = Saver(database)
	saver.save(field, data)

@saver_cli.command()
@click.option('--database', '-d', help = 'Database url')
@click.option('--queue_url', '-q', help = 'queue_url')
def run_saver(database_url, queue_url):
	saver = Saver(database_url)
	queue = furl(queue_url)
	mq = queue.scheme
    mq_host = queue.host
    mq_port = queue.port
    publisher = saver.save
    mq_exchange = "Results"

class Saver:
	def __init__(self, database_url):
		self.savers = self.get_savers()
		url = furl(database_url)
		self.db_type = url.scheme
		self.db_host = url.host
		self.db_port = url.port
		if self.db_type in self.types:
			self.saver = self.savers[saver](host = self.db_host, port = self.db_port)
		else:
			print(f"Saver {saver} wasn't found")
			raise KeyError()
	
	def save(self, topic, data):
		self.saver.save(topic, data)

	def get_savers(self):
		utils = Path(__file__).parent.absolute()/'utils'
        savers = utils/'savers'
        sys.path.insert(0, str(utils))
        self.savers = {}
        self.types = {}
        for saver in savers.iterdir():
            if not 'saver' in saver.name:
                continue
            m = importlib.import_module(f'{savers.name}.{saver.stem}')
            try:
                m = m.__dict__[camel_from_snake(saver.stem)]
            except Exception as e:
                print(f"{savers.name}.{saver.stem} in wrong format" , e)
                continue
            self.savers[saver.stem] = m
            if 'type' in m.__dict__:
            	self.types[m.__dcit__['type']] = m