import threading
import logging
from pathlib import Path
from struct import unpack
import click
from .cli import server
from .utils import Listener
from .thought import Thought
from .utils import Hello, Config, Snapshot
from .utils import read_string, Parser
from PIL import Image
import json
from datetime import datetime
from functools import reduce
from .utils import Config_handler
parser = Parser()
logging.basicConfig(format = '%(levelname).1s %(asctime)s %(message)s',
					datefmt = '%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('server_I')
logger.setLevel(logging.INFO)

def reverse(tup):
	a,b,c = tup
	return (c, b, a)

@server.command()
@click.option('--host', '-h', help = 'Host ip', default = '127.0.0.1')
@click.option('--port', '-p', help = 'Host port', default = '8000')
@click.option('--data', '-d', help = 'The path to data dictionary', default = 'data')
@click.option('--config', '-c', help = 'Config file', default = None)
def run_server(host = '127.0.0.1', port = '8000', data = 'data', config = None):
	if config:
		logger.info("Reading config file")
		config = Config_handler(config, 'server')
		port = config.port
		host = config.host
		data = config.data
	server = Listener(int(port), host)
	server.start()
	logger.info("Server started")
	p = Path(data)
	if p.is_file():
		raise Exception('data is a file and not a directory')
	while True:
		client = server.accept()
		t = threading.Thread(target=session_handler, args=(client, p))
		t.start()
	server.stop()
	logger.info("Server stopped")


def session_handler(client, path):
	while(True):
		fields = parser.parsers.keys()
		lock = threading.Lock()
		try:
			hi_message = client.receive_message()
		except Exception:
			logger.info("bad hello message")
			return
		try:
			hello = Hello.deserialize(hi_message)
		except Exception as e:
			logger.debug("Hello:", e)
			return
		logger.info('got hello')
		logger.debug(f'Fields: {fields}')
		config = Config(fields)
		client.send_message_to_addr(config.serialize())
		logger.info('sent config')
		try:
			snap_message = client.receive_message()
		except Exception:
			logger.debug("bad snapshot")
			return
		try:
			snapshot = Snapshot.deserialize(snap_message)
		except Exception as e:
			debug_logger.debug("Snapshot:", e)
			return
		logger.info('got snapshot')
		lock.acquire()
		p = path / f'{hello.user_id}'
		p.mkdir(exist_ok=True)
		p = p / f"{datetime.fromtimestamp(snapshot.timestamp/1000).strftime('%Y-%m-%d_%H-%M-%S.%f')}"
		p.mkdir(exist_ok=True)
		parser.parse(fields ,snapshot, p)
		lock.release()
		logger.debug('done')


if __name__ == '__main__':
	server()
