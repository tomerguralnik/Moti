from furl import furl
from pathlib import Path
import importlib
import sys
from .misc import camel_from_snake

class DatabaseReader:
    """
    DatabaseReader is a reader for a general database
    One can choose which reader they want to use
    for example: mongo_reader that is in dbreaders directory
    A reader must have the following methods:
    reader.find(collection, filters): finds all entries in the collection that pass the filters
    reader.find_one(collection, filters): finds one entry in the collection that pass the filters
    A reader must also have a 'db' class variable which is basically it's name 
    """
    def __init__(self, database_url):
        """
        Initiates a dbreader that database_url specifies

        :param database_url: "db://host:port"
            reader: has to be equal to 'db' field of desired dbreader
            host:port: are the host and port the database
        :type database_url: str
        """
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
        """
        Find all entries in the collection that pass the filters

        :param collection: the collection to access
        :type collection: str
        :param filters: the filters to apply on the search (usally a dictionary), defaults to None
        :type filters: dict(,optional)
        
        :return: a list of all results in the collection that match the filters
        :rtype: list
        """
        return self.reader.find(collection, filters)

    def find_one(self, collection, filters = None):
        """
        Find an entry in the colleciton that passes the filters

        :param collection: the collection to access
        :type collection: str
        :param filters: the filters to apply on the search (usally a dictionary), defaults to None
        :type filters: dict(,optional)
        
        :return: a list of all results in the collection that match the filters
        :rtype: list
        """
        return self.reader.find_one(collection, filters)

    def get_readers(self):
        """
        Import all dbreaders in ./utils/dbreaders
        Every dbreader should have 'reader' in the name of it's file
        Only one dbreader per file
        The name of file should be in snake case
        The name of dbreader should be in camel case and the same as file's name
        The dbreader should have 'db' variable so it can be chosen by that variable
        """
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