from .utils import Publisher
from .server import run_server
from pathlib import Path
import threading
from .utils import Parser
from .utils import Consumer
publisher = Publisher(['Results'], 'rabbitmq_parser_publisher', name = 'Publish')
con = Consumer(Path(__file__).parent.parent.absolute()/'data', publish_factory =  publisher)
con.consume()
