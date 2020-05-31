from furl import furl
from pathlib import Path
import sys
import importlib
from .misc import camel_from_snake
class Consumer:
    """
    A consumer is basically a generalized message queue consumer
    One can choose which consumer they want to use 
    for example: the rabbitmq_consumer that is in the consumers directory
    A consumer must have the following methods:
    consumer.add_queue(queue, callback): which tells the consumer how to consume the queue
    consumer.consume(): which makes the consumer to start consuming on all queues added
    A consumer must have a class variable 'protocol' which is basically it's name
    """
    def __init__(self, mq_url):
        """
        Initiates a consumer that mq_url specifies

        :param mq_url: "protocol://host:port/exchange"
            protocol: has to be equal to 'protocol' field of desired consumer
            host:port: are the host and port the mq
            exchange: is the exchange the queues should belong to
        :type mq_url: str
        """
        self.get_consumers()
        queue = furl(mq_url)
        self.consumer = self.consumers[queue.scheme](host = queue.host, port = queue.port, exchange_name = str(queue.path)[1:])

    def add_queue(self, queue, callback):
        """
        Adds the queue to the consumer with the callback function
        
        :param queue: name of queue
        :type queue: str
        :param callback: callback function for queue consumption
        :type callback: callable
        """
        self.consumer.add_queue(queue, callback)

    def consume(self):
        """
        Start consuming
        """
        self.consumer.consume()
        
    def get_consumers(self):
        """
        Import all consumers in ./utils/consumers
        Every consumer should have 'consumer' in the name of it's file
        Only one consumer per file
        The name of file should be in snake case
        The name of consumer should be in camel case and the same as file's name
        The consumer should have 'protocol' variable so it can be chosen by that variable
        """
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