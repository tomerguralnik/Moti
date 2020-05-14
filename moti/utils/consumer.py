from furl import furl
from pathlib import Path
import sys
import importlib
from .misc import camel_from_snake
class Consumer:
    def __init__(self, mq_url):
        #mq_url = "protocol://host:port/exchange"
        self.get_consumers()
        queue = furl(mq_url)
        self.consumer = self.consumers[queue.scheme](host = queue.host, port = queue.port, exchange_name = str(queue.path)[1:])

    def add_queue(self, queue, callback):
        self.consumer.add_queue(queue, callback)

    def consume(self):
        self.consumer.consume()
        
    def get_consumers(self):
        utils = Path(__file__).parent.absolute()
        consumers = utils/'consumers'
        sys.path.insert(0, str(utils))
        self.consumers = {}
        for consumer in consumers.iterdir():
            if not 'consumer' in consumer.name:
                continue
            m = importlib.import_module(f'{consumers.name}.{consumer.stem}')
            try:
                m = m.__dict__[camel_from_snake(consumer.stem)]
            except Exception as e:
                print(f"{consumers.name}.{consumer.stem} in wrong format" , e)
                continue
            if 'protocol' in m.__dict__:
                self.consumers[m.__dict__['protocol']] = m