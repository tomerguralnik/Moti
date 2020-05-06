from .utils import Consumer
from .utils import Parser
from .cli import parsing
from pathlib import Path
from furl import furl
from .utils import Publisher
import click

data_dir = Path(__file__).parent.parent.absolute()/'data'

def run_parser(field, data):
    parsers = Parser()
    return parsers.parse_field(field, data, data_dir)

@parsing.command()
@click.option('--field', '-f', help='Which field to parse')
@click.option('--data', '-d', help='Data to pass to the parser')
def parse(field, data):
    with open(data, 'r') as file:
        print(run_parser(field, file.read()))

@parsing.command(name = 'run-parser')
@click.option('--field', '-f', help = 'Which field to parse')
@click.option('--url', '-u', help = 'Url to message queue')
def run_parser_cli(field, url):
    parsers = Parser()
    url = furl(url)
    mq = url.scheme + '_consumer'
    mq_host = url.host
    mq_port = url.port
    publisher = Publisher([parser.__name__ for parser in parsers.mapping[field]], mq, path = data_dir, host = mq_host, port = mq_port, name ='Results')
    consumer = Consumer(data_dir, host = mq_host, port = mq_port, parsers = parsers.mapping[field], publish_factory = publisher)
    consumer.consume()






if __name__ == '__main__':
    parsing()