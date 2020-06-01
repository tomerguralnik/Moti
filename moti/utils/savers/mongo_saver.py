from pymongo import MongoClient
import json
import threading

class MongoSaver:
    """
    This saver saves all the user data to the users collection
    and all the snapshot data to the snapshots collection
    Every user has a list of his snapshots, every snapshot in that
    list is represented as it's timestamp which is equivalent to it's id 
    """
    protocol = 'mongodb'
    def __init__(self, host = '127.0.0.1', port = 27017):
        """
        :param host: ip of db
        :type host: str
        :param port: port of db
        :type port: int
        """
        self.client = MongoClient(host, port)
        self.db = self.client.snapshot_database
        self.users = self.db.users
        self.snapshots = self.db.snapshots
        self.lock = threading.Lock()

    def save(self, topic, data):
        """
        :param topic: the field data belongs to
        :type topic: str
        :param data: a json string passed from a parser
        :type topic: json string 
        """
        snap = json.loads(data)
        user_deets = snap['user']
        timestamp = snap['timestamp']
        field = snap[topic]
        self.lock.acquire()
        user = self.users.find_one(user_deets)
        if not user:
            self.users.insert_one({**user_deets, 'snapshots': [timestamp]})
        else:
            self.users.update_one(user_deets,{'$addToSet': {'snapshots': timestamp}})
        user_id = user_deets['user_id']
        snapshot = self.snapshots.find_one({'user_id': user_id,
                                            'timestamp': timestamp})
        if not snapshot:
            self.snapshots.insert_one({'user_id': user_id,
                                       'timestamp': timestamp,
                                       'ID': timestamp,
                                       topic: field,
                                       'fields': [topic]})
        else:
            self.snapshots.update_one({'user_id': user_id, 'timestamp': timestamp}, 
                                      {'$set': {topic: field}, '$addToSet': {'fields': topic}})
        self.lock.release()



