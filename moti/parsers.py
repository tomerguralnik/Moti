from .utils import Consumer
from .utils import Parser
from pathlib import Path
from furl import furl
from .utils import Publisher, Transfer, Config_handler
import click

@click.group()
def parsing():
    pass

data_dir = Path(__file__).parent.parent.absolute()/'data' #The directory that parsers save their files to

def run_parser(field, data):
    """
    :param field: name of a field
    :type field: str
    :param data: data to parse
    :type data: encoded path

    :return: parsed data
    :rtype: json string
    """
    parsers = Parser()
    return parsers.parse_field(field, data, data_dir)

@parsing.command()
@click.argument('field', type = click.STRING)
@click.argument('data', type = click.STRING)
def parse(field, data):
    print(run_parser(field, data.encode('ascii')))

@parsing.command(name = 'run-parser')
@click.argument('field', type = click.STRING)
@click.argument('url', nargs = -1, type = click.STRING)
@click.option('--config', '-c', help = 'Config file', default = None)
def run_parser_cli(field, url, config = None):
    if config:
        config = Config_handler(config, 'parsers')
        url = config.queue
    else:
        url = url[0]
    parsers = Parser([field])
    purl = furl(url)
    purl.scheme = purl.scheme + '_parser'
    purl = str(purl)
    queues = parsers.generate_queues()
    publisher = Publisher(queues, purl, path = data_dir, name = 'Results', parsers = parsers)
    transfer = Transfer(url + 'Server', queues, publish_factory = publisher)
    transfer.start()


@parsing.command()
@click.argument('url', nargs = -1, type = click.STRING)
@click.option('--config', '-c', help = 'Config file', default = None)
def run_all_parsers(url, config = None):
    """
    This function runs all parsers
    """
    if config:
        config = Config_handler(config, 'parsers')
        url = config.queue
    else:
        url = url[0]
    parsers = Parser()
    purl = furl(url)
    purl.scheme = purl.scheme + '_parser'
    purl = str(purl)
    queues = parsers.generate_queues()
    publisher = Publisher(queues, purl, path = data_dir, name = 'Results', parsers = parsers)
    transfer = Transfer(url + 'Server', queues, publish_factory = publisher)
    transfer.start()





if __name__ == '__main__':
    parsing()
