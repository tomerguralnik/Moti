import pymongo
from pymongo import MongoClient
import json
class MongoSaver:
	protocol = 'mongo'
	def __init__(self, host = '127.0.0.1', port = 27016):
		self.client = MongoClient(host, port)
		self.db = self.client.snapshot_database

	def save(self, topic, data):
		if not topic in collections:
			self.collections[topic] = self.
		snap = json.loads(data)
		snap['topic': topic]
		self.collection.insert_one(snap)

