from flask import Flask, render_template, request, redirect, flash
from furl import furl
from .utils import DatabaseReader
import json
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import click
@click.group()
def api():
	pass

app = Flask(__name__)
'''
uploads = Path(__file__).parent.parent /'data'/'uploads'
uploads.mkdir(exist_ok = True)
app.config['UPLOAD_FOLDER'] = uploads.absolute() #data/uploads
ALLOWED_SUFFIXES = ['.txt', '.jpg', '.png', '.pdf', '.jpeg', '.gif']
'''


class API:
	def __init__(self, host, port, database_url):
		self.db = DatabaseReader(database_url)
		self.host = host
		self.port = port

	def get_users(self):
		all_users = self.db.find('users')
		return [{'ID': user['user_id'], 'Name': user['user_name']} for user in all_users]

	def get_user(self, user_id):
		user = self.db.find_one('users', {'user_id': user_id})
		return {'ID': user['user_id'],
				'name': user['user_name'],
				'birthday': user['birth_date'],
				'gender': user['gender'] }

	def get_snapshots(self, user_id):
		user = self.db.find_one('users', {'user_id': user_id})
		snapshots = user['snapshots']
		return [{'ID': timestamp,
				 'timestamp' : timestamp} for timestamp in snapshots]

	def get_snapshot(self, user_id, snapshot_id):
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
		user = self.db.find_one('users', {'user_id': user_id})
		snapshot = self.db.find_one('snapshots', {'ID': snapshot_id, 'user_id': user['user_id']})
		return {result_name: snapshot[result_name]}

	def setup(self):
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
			for key in {**result}:
				if not isinstance(result[key], str):
					continue
				path = Path(result[key])
				if not path.exists():
					continue
				if not path.is_file():
					continue
				result[key + '_url'] = f'/users/{user_id}/snapshots/{snapshot_id}/{result_name}/{key}'
			return json.dumps(self.get_result(user_id, snapshot_id, result_name))

		@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/<file_field>', methods = ['GET'])
		def get_result_file_flask(user_id, snapshot_id, result_name, file_field):
			user_id = int(user_id)
			snapshot_id = int(snapshot_id)
			result = self.get_result(user_id, snapshot_id, result_name)
			with open(result[file_field],'rb') as file:
				return file.read()


@api.command(name = 'run-server')
@click.option('--host', '-h', help = 'Ip', default = '127.0.0.1')
@click.option('--port', '-p', help =  'Port', default = 8000 )
@click.option('--database', '-d', help = 'Database url', default = 'mongodb://127.0.0.1:27017/')
def run_api_server(host, port, database):
	API(host, port, database).setup()
	app.run(host = host, port = port)

if __name__ == '__main__':
	api()