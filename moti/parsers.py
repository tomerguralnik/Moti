from .utils import Consumer
from .utils import Parser
from pathlib import Path
from furl import furl
from .utils import Publisher, Transfer
import click

@click.group()
def parsing():
    pass

data_dir = Path(__file__).parent.parent.absolute()/'data'

def run_parser(field, data):
    parsers = Parser()
    return parsers.parse_field(field, data, data_dir)

@parsing.command()
@click.argument('field', type = click.STRING)
@click.argument('data', type = click.STRING)
def parse(field, data):
    with open(data, 'r') as file:
        print(run_parser(field, file.read()))

@parsing.command(name = 'run-parser')
@click.argument('field', type = click.STRING)
@click.argument('url', type = click.STRING)
def run_parser_cli(field, url):
    parsers = Parser([field])
    purl = furl(url)
    purl.scheme = purl.scheme + '_parser'
    purl = str(purl)
    queues = parsers.generate_queues()
    publisher = Publisher(queues, purl, path = data_dir, name = 'Results', parsers = parsers)
    transfer = Transfer(url + 'Server', queues, publish_factory = publisher)
    transfer.start()

@parsing.command()
@click.argument('url', type = click.STRING)
def run_all_parsers(url):
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
