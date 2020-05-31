from pymongo import MongoClient
import json
import threading

class MongoReader:
    db = 'mongodb'
    def __init__(self, host, port):
        """
        :param host: ip of the db
        :type host: str
        :param port: port of the db
        :type port: int
        """
        self.client = MongoClient(host, port)
        self.db = self.client.snapshot_database

    def find_one(self, collection, dic = None):
        """
        Return one entry from the specified collection that matches dic

        :param collection: name of collectio
        :type collection: str
        :param dic: a dictionary of filters, defaults to None
        :type dic: dict or None(,optional)
        """
        return self.db[collection].find_one(dic)

    def find(self, collection, dic = None):
        """
        Return every entry from the specified collection that matches dic

        :param collection: name of collectio
        :type collection: str
        :param dic: a dictionary of filters, defaults to None
        :type dic: dict or None(,optional)
        """
        return self.db[collection].find(dic)