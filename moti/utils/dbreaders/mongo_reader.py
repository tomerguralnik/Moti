from pymongo import MongoClient
import json
import threading

class MongoReader:
	db = 'mongodb'
	def __init__(self, host, port):
		self.client = MongoClient(host, port)
		self.db = self.client.snapshot_database
		self.lock = threading.Lock()

	def find_one(self, collection, dic = None):
		return self.db[collection].find_one(dic)

	def find(self, collection, dic = None):
		return self.db[collection].find(dic)