from .misc import camel_from_snake
import importlib
from pathlib import Path
from furl import furl
import sys

class Publisher:
    """
    Publisher is a general publisher of data
    One can choose which publisher they want to use 
    for example: the rabbitmq_parser_publisher that is in the publishers directory
    A publisher must have one of the following methods:
    publisher.publish(snapshot): which publishes with snapshot
    publisher.publish_factory(snapshot, queue): which publishes the snapshot to a specific queue
        the publish_factory method can also change the format of publishing depending on the queue
    A publisher must have a class variable 'protocol' which is basically it's name 
    """
    def __init__(self, queues, mq_url, path = None, name = 'Server', parsers = None):
        """
        :param queues: a list of queues to publish to
        :type queues: list
        :param mq_url: 'protocol://host:port/'
            protocol: has to be equal to 'protocol' field of desired publisher
            host:port: are the host and port the mq
        :param path: some publishers need a path to save their files to, defaults to None
        :type path: str or None(,optional)
        :param name: some publishers need to know what exchange name to publish to, defaults to 'Server'
        :type name: str(,optional)
        :param parsers: some publishers use parsers to publish the snapshot, defaults to None
        :type parsers: str or None(,optional)
        """
        self.get_publishers()
        queue = furl(mq_url)
        protocol = queue.scheme
        host = queue.host
        port = queue.port
        if protocol in self.publishers:
            if parsers:
                self.publisher = self.publishers[protocol](queues, host, port, path, name, parsers)
            else:
                self.publisher = self.publishers[protocol](queues, host, port, path, name)
        else:
            print(f"protocol {protocol} does'nt fit any current protocol or publisher")
            raise KeyError('publisher was not found')

    def __call__(self, snapshot, queue = None):
        """
        Calls publish factory if the publisher has a publish_factory method
        otherwise calls publish

        :param snapshot: some data
        :type snapshot: object
        :param queue: a queue name, defaults to None
        :type queue: str or None(,optional)
        """

        try:
            return self.publisher.publish_factory(snapshot, queue)
        except AttributeError:
            pass
        try:
            return self.publisher.publish(snapshot)
        except AttributeError:
            raise Exception("No publishing method given!")


    def get_publishers(self):
        """
        Import all publishers in ./utils/publishers
        Every publisher should have 'publisher' in the name of it's file
        Only one publisher per file
        The name of file should be in snake case
        The name of publisher should be in camel case and the same as file's name
        The publisher should have 'protocol' variable so it can be chosen by that variable
        """
        utils = Path(__file__).parent.absolute()
        publishers = utils/'publishers'
        sys.path.insert(0, str(utils))
        self.publishers = {}
        for publisher in publishers.iterdir():
            if not 'publisher' in publisher.name:
                continue
            m = importlib.import_module(f'{publishers.name}.{publisher.stem}')
            try:
                m = m.__dict__[camel_from_snake(publisher.stem)]
            except Exception as e:
                print(f"{publishers.name}.{publisher.stem} in wrong format" , e)
                continue
            if 'protocol' in m.__dict__:
                self.publishers[m.__dict__['protocol']] = m
