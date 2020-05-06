from .misc import camel_from_snake
import importlib
from pathlib import Path
import sys

class Publisher:
    def __init__(self, queues, publisher, path = None, host = '127.0.0.1', port = 5672, name = 'Server'):
        self.get_publishers()
        if publisher in self.publishers:
            self.publisher = self.publishers[publisher](queues, host, port, path, name)
        elif publisher in self.protocols:
            self.publisher = self.protocols[publisher](queues, host, port, path, name)
        else:
            print(f"publisher {publisher} does'nt fit any current protocol or publisher")
            raise KeyError('publisher was not found')

    def __call__(self, snapshot, parser = None):
        try:
            return self.publisher.publish(snapshot)
        except AttributeError:
            print("No publisher")
        try:
            return self.publisher.publish_factory(snapshot, parser)
        except AttributeError:
            raise Exception("No publishing method given!")


    def get_publishers(self):
        utils = Path(__file__).parent.absolute()
        publishers = utils/'publishers'
        sys.path.insert(0, str(utils))
        self.publishers = {}
        self.protocols = {}
        for publisher in publishers.iterdir():
            if not 'publisher' in publisher.name:
                continue
            m = importlib.import_module(f'{publishers.name}.{publisher.stem}')
            try:
                m = m.__dict__[camel_from_snake(publisher.stem)]
            except Exception as e:
                print(f"{publishers.name}.{publisher.stem} in wrong format" , e)
                continue
            self.publishers[publisher.stem] = m
            if 'protocol' in m.__dict__:
                self.protocols[m.__dict__['protocol']] = m
