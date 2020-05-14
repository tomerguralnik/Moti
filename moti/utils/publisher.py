from .misc import camel_from_snake
import importlib
from pathlib import Path
from furl import furl
import sys

class Publisher:
    def __init__(self, queues, mq_url, path = None, name = 'Server', parsers = None):
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
        try:
            return self.publisher.publish(snapshot)
        except AttributeError:
            #TODO: logging
            pass
        try:
            return self.publisher.publish_factory(snapshot, queue)
        except AttributeError:
            raise Exception("No publishing method given!")


    def get_publishers(self):
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
