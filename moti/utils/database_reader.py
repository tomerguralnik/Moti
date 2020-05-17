from furl import furl
from pathlib import Path
import importlib
import sys
from .misc import camel_from_snake

class DatabaseReader:
    def __init__(self, database_url):
        self.get_readers()
        url = furl(database_url)
        self.db_type = url.scheme
        self.db_host = url.host
        self.db_port = url.port
        if self.db_type in self.types:
            self.reader = self.types[self.db_type](host = self.db_host, port = self.db_port)
        else:
            print(f"Saver {self.db_type} wasn't found")
            raise KeyError()

    def find(self, collection, filters = None):
        return self.reader.find(collection, filters)

    def find_one(self, collection, filters = None):
        return self.reader.find_one(collection, filters)

    def get_readers(self):
        utils = Path(__file__).parent.absolute()
        readers = utils/'dbreaders'
        sys.path.insert(0, str(utils))
        self.types = {}
        for reader in readers.iterdir():
            if not 'reader' in reader.name:
                continue
            m = importlib.import_module(f'{readers.name}.{reader.stem}')
            try:
                m = m.__dict__[camel_from_snake(reader.stem)]
            except Exception as e:
                print(f"{readers.name}.{reader.stem} in wrong format" , e)
                continue
            if 'db' in m.__dict__:
                self.types[m.__dict__['db']] = m