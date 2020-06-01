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
@click.option('--database', '-d', help = "the database's url" ,type = click.STRING, default = 'mongodb://127.0.0.1:27017/' )
@click.argument('field', type = click.STRING)
@click.argument('data', type = click.STRING)
def save(field, data, database):
    saver = Saver(database)
    saver.save(field, data)

@saver_cli.command()
@click.argument('database_url', nargs = -1, type = click.STRING)
@click.option('--config', '-c', help = 'Config file')
def run_saver(database_url, queue_url = None, config = None):
    """
    If config is provided then it overrides all other variables

    This function sets up a Transfer that transfers data from queue_url
    to database_url with a saver as it's publishing function 

    :param database_url: a url to a database format described in Saver
    :type database_url: str
    :param queue_url: a url to a message queue 
    :type queue_url: str
    :param config: a config file, defaults to None
    :type config: str(,optional)
    """
    if config:
        config = Config_handler(config, 'saver')
        database_url = config.db
        queue_url = config.queue
    elif len(database_url) == 2:
        database_url, queue_url = database_url
    elif len(database_url) > 2:
        print('usage: run-saver <database_url> <queue_url>')
        print('usage: run-saver -c <config>')
        return None
    saver = Saver(database_url)
    parsers = Parser()
    transfer = Transfer(queue_url + 'Results', parsers.generate_queues(), publish_factory = lambda snapshot, queue: saver.save(queue.split('/')[-2], snapshot))
    transfer.start()

class Saver:

    def __init__(self, database_url):
        """
        Every saver class should be initialized by host and port
        and have a save(topic, data) method

        :params database_url: protocol://host:port
            protocol is the db type
            host and port are ip:port
            example: mongodb://127.0.0.1:8000
            protocol should match the 'protocol' variable of desired saver
        :type database_url: str
        """
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
        self.saver.save(topic, data)

    def get_savers(self):
        """
        Import all savers in ./utils/savers
        Every saver should have 'saver' in the name of it's file
        Only one saver per file
        The name of file should be in snake case
        The name of saver should be in camel case and the same as file's name
        The saver should have 'protocol' variable so it can be chosen by that variable
        """
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