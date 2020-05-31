from flask import Flask, render_template, request, redirect, flash, send_file
from flask_cors import CORS
from furl import furl
from .utils import DatabaseReader
import json
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import click
from .utils import Config_handler

@click.group()
def api():
    pass

app = Flask(__name__)
CORS(app)

'''
uploads = Path(__file__).parent.parent /'data'/'uploads'
uploads.mkdir(exist_ok = True)
app.config['UPLOAD_FOLDER'] = uploads.absolute() #data/uploads
ALLOWED_SUFFIXES = ['.txt', '.jpg', '.png', '.pdf', '.jpeg', '.gif']
'''
def generate_urls(dic, url):
    """
    For every path to a file in dic add an entry containing
    it's designated url

    :param dic: a dictionary
    :type dic: dict
    :param url: a base url string
    :type url: str
    """
    url_dic = {}
    for key in dic:
        if is_file(dic[key]):
            url_dic[key + '_url'] = f'{url}/{key}'
    for key in url_dic:
        dic[key] = url_dic[key]

def get_all_files(dic, current):
    """
    Iterating over current dictionary going recursivly into every dictionary inside
    if a key: path to file entry is found somewhere inside current then key: path to file
    is added to top level of dic

    :param dic: a dictionary
    :type dic: dict
    :param current: a dictionary, should be a copy of dic for first call
    :type current: dict
    """
    for key in current:
        if is_file(current[key]):
            dic[key] = current[key]
        elif isinstance(current[key], dict):
            get_all_files(dic, current[key])


    
def is_file(val):
    """
    :param val: anything
    :type val: Object

    :return: True if val is an existing file, False otherwise
    :rtype: bool
    """
    if not isinstance(val, str):
        return False 
    path = Path(val)
    if not path.exists():
        return False
    if not path.is_file():
        return False
    return True

class API:
    def __init__(self, host, port, database_url):
        """
        :param host: ip to host api at
        :type host: str
        :param port: port to host api at
        :type port: str or int
        :param database_url: a url to a database for the api to use
        :tyoe database_url: str
        """
        self.db = DatabaseReader(database_url)
        self.host = host
        self.port = port

    def get_users(self):
        """
        :return: A list of all users in the database
        :rtype: list
        """
        all_users = self.db.find('users')
        return [{'ID': user['user_id'], 'Name': user['user_name']} for user in all_users]

    def get_user(self, user_id):
        """
        :param user_id: a user id
        :type user_id: int or str

        :return: a dictionary with all personal information of the user
        :rtype: dict
        """
        user = self.db.find_one('users', {'user_id': user_id})
        return {'ID': user['user_id'],
                'name': user['user_name'],
                'birthday': user['birth_date'],
                'gender': user['gender'] }

    def get_snapshots(self, user_id):
        """
        :param user_id: a user id
        :type user_id: int or str

        :return: A list of all snapshots correlated to user
        :rtype: list
        """
        user = self.db.find_one('users', {'user_id': user_id})
        snapshots = user['snapshots']
        return [{'ID': timestamp,
                 'timestamp' : timestamp} for timestamp in snapshots]

    def get_snapshot(self, user_id, snapshot_id):
        """
        :param user_id: a user id
        :type user_id: int or str
        :param snapshot_id: a snapshot id
        :type snapshot_id: int or str

        :return: A dictionary representing the snapshot
        :rtype: dict
        """
        user = self.db.find_one('users', {'user_id': user_id})
        snapshot = self.db.find_one('snapshots', {'ID': snapshot_id, 'user_id': user['user_id']})
        if not snapshot:
            return None
        del snapshot['user_id']
        del snapshot['fields']
        if '_id' in snapshot.keys():
            del snapshot['_id']
        return snapshot

    def get_result(self, user_id, snapshot_id, result_name):
        """
        :param user_id: a user id
        :type user_id: int or str
        :param snapshot_id: a snapshot id
        :type snapshot_id: int or str
        :param result_name: a field name
        :type result_name: str
        :return: A dictionary representing the field of the snapshot
            This dictionary also has a copy of all files in the dictionary
            found in the database on it's top level
        :rtype: dict
        """
        user = self.db.find_one('users', {'user_id': user_id})
        snapshot = self.db.find_one('snapshots', {'ID': snapshot_id, 'user_id': user['user_id']})
        ret = {result_name: snapshot[result_name]}
        get_all_files(ret, {**ret})
        return ret

    def setup(self):
        """
        This functions uses the basic API functions
        changing them to a desired format and routing with flask
        """
        @app.route('/users', methods = ['GET'])
        def get_users_flask():
            return json.dumps(self.get_users())

        @app.route('/users/<user_id>', methods = ['GET'])
        def get_user_flask(user_id):
            user_id = int(user_id)
            return json.dumps(self.get_user(user_id))

        @app.route('/users/<user_id>/snapshots', methods = ['GET'])
        def get_snapshots_flask(user_id):
            user_id = int(user_id)
            return json.dumps(self.get_snapshots(user_id))

        @app.route('/users/<user_id>/snapshots/<snapshot_id>', methods = ['GET'])
        def get_snapshot_flask(user_id, snapshot_id):
            user_id = int(user_id)
            snapshot_id = int(snapshot_id)
            return json.dumps(self.get_snapshot(user_id, snapshot_id))

        @app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>', methods = ['GET'])
        def get_result_flask(user_id, snapshot_id, result_name):
            user_id = int(user_id)
            snapshot_id = int(snapshot_id)
            result = self.get_result(user_id, snapshot_id, result_name)
            base_url = f'http://{self.host}:{self.port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}'
            generate_urls(result, base_url)
            return json.dumps(result)

        @app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/<file_field>', methods = ['GET'])
        def get_result_file_flask(user_id, snapshot_id, result_name, file_field):
            user_id = int(user_id)
            snapshot_id = int(snapshot_id)
            result = self.get_result(user_id, snapshot_id, result_name)
            return send_file(result[file_field])


@api.command(name = 'run-server')
@click.option('--host', '-h', help = 'Ip', default = '127.0.0.1')
@click.option('--port', '-p', help =  'Port', default = 5000 )
@click.option('--database', '-d', help = 'Database url', default = 'mongodb://127.0.0.1:27017/')
@click.option('--config', '-c', help = 'Config file', default = None)
def run_api_server(host, port, database, config = None):
    if config:
        config = Config_handler(config, 'api')
        host = config.host
        port = config.port
        database = config.db
    API(host, int(port), database).setup()
    app.run(host = host, port =int(port))

if __name__ == '__main__':
    api()
