from pathlib import Path
from struct import unpack
from datetime import datetime
from struct import unpack
import importlib
import sys
from .misc import camel_from_snake

class Reader:
    """
    Reader is a general reader of data
    One can choose which reader they want to use 
    for example: the proto_reader that is in the readers directory
    A reader must have the following methods:
    reader.get_user(): which reads the user details from the smaple file
    reader.get_snapshot(): which reads the next snapshot and returns a dict object
    A reader must have a class variable 'reader' which is basically it's name 
    """
    def __init__(self, path, reader):
        """
        :param path: path to sample
        :type path: str
        :param reader: reader name
        :type reader: str
        """
        self.get_readers()
        try:
            self.reader = self.readers[reader](path)
        except KeyError as e:
            print(f"Reader {reader} wasn't found")
            raise(e)
        user = self.reader.get_user()
        for field in user:
            self.__dict__[field] = user[field]

    def __iter__(self):
        return self

    def __next__(self):
        """
        Get next snapshot
        """
        return ReaderSnapshot(self.reader.get_snapshot())

    def get_readers(self):
        """
        Import all readers in ./utils/readers
        Every reader should have 'reader' in the name of it's file
        Only one reader per file
        The name of file should be in snake case
        The name of reader should be in camel case and the same as file's name
        The reader should have 'reader' variable so it can be chosen by that variable
        """
        utils = Path(__file__).parent.absolute()
        readers = utils/'readers'
        sys.path.insert(0, str(utils))
        self.readers = {}
        for reader in readers.iterdir():
            if not 'reader' in reader.name:
                continue
            m = importlib.import_module(f'{readers.name}.{reader.stem}')
            try:
                self.readers[reader.stem] = m.__dict__[camel_from_snake(reader.stem)]
            except Exception as e:
                print(f"{readers.name}.{reader.stem} in wrong format" , e)


class ReaderSnapshot:
    """
    Trun the dictionary from get_snapshot into a class for convinience
    """
    def __init__(self, dic):
        """
        :param dic: a dictionary to capture
        :type dic: dict or dict-like type object
        """
        self.params =  dic

    def __repr__(self):
        ret = ''
        for key in self.params:
            ret += f'{key}: {self.params[key]}\n'
        return ret

    def __getattr__(self, val):
        """
        If a value isn't found in self.__dict__ the look inside self.params

        :param val: anything

        :return: the item associated with val
        """
        if val in self.__dict__:
            return self.__dict__[val]
        elif val in self.params:
            return self.params[val]
        else:
            raise Exception(f'No such param {val}')
