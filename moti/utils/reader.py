from pathlib import Path
from struct import unpack
from datetime import datetime
from struct import unpack
import importlib
import sys
from .misc import camel_from_snake

class Reader:

    def __init__(self, path, reader):
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
        try:
            return ReaderSnapshot(self.reader.get_snapshot())
        except Exception as e:
            raise e

    def get_readers(self):
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
    def __init__(self, dic):
        self.params =  dic

    def __repr__(self):
        ret = ''
        for key in self.params:
            ret += f'{key}: {self.params[key]}\n'
        return ret

    def __getattr__(self, val):
        if val in self.__dict__:
            return self.__dict__[val]
        elif val in self.params:
            return self.params[val]
        else:
            raise Exception(f'No such param {val}')
