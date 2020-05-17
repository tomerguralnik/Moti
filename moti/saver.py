from furl import furl
from pathlib import Path
import importlib
import click
from .utils import Transfer, Parser
import sys
from .utils import camel_from_snake, Config_handler

@click.group()
def saver_cli():
    pass
    
@saver_cli.command()
@click.argument('database')
@click.argument('field')
@click.argument('data')
def save(database, field, data):
    saver = Saver(database)
    saver.save(field, data)

@saver_cli.command()
@click.argument('database_url', nargs = -1)
@click.option('--config', '-c', help = 'Config file')
def run_saver(database_url, queue_url = None, config = None):
    if config:
        config = Config_handler(config, 'saver')
        database_url = config.db
        queue_url = config.queue
    elif len(database_url) == 2:
        database_url, queue_url = database_url
    elif len(database_url) > 2:
        #TODO:USAGE MESSAGE
        return None
    saver = Saver(database_url)
    parsers = Parser()
    transfer = Transfer(queue_url + 'Results', parsers.generate_queues(), publish_factory = lambda snapshot, queue: saver.save(queue.split('/')[-2], snapshot))
    transfer.start()

class Saver:
    def __init__(self, database_url):
        self.get_savers()
        url = furl(database_url)
        self.db_type = url.scheme
        self.db_host = url.host
        self.db_port = url.port
        if self.db_type in self.types:
            self.saver = self.types[self.db_type](host = self.db_host, port = self.db_port)
        else:
            print(f"Saver {self.db_type} wasn't found")
            raise KeyError()
    
    def save(self, topic, data):
        print(f"{topic} - save")
        self.saver.save(topic, data)

    def get_savers(self):
        utils = Path(__file__).parent.absolute()/'utils'
        savers = utils/'savers'
        sys.path.insert(0, str(utils))
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
            if 'protocol' in m.__dict__:
                self.types[m.__dict__['protocol']] = m


if __name__ == '__main__':
    saver_cli()