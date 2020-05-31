import click
import requests
@click.group()

def cli():
	pass

@cli.command()
@click.option('--host', '-h', help = 'Api IP', default = '127.0.0.1')
@click.option('--port', '-p', help = 'Api port', default = 8000)
def get_users(host = '127.0.0.1', port = 8000):
	req = requests.get(f'http://{host}:{port}/users')
	print(req.text)

@cli.command()
@click.option('--host', '-h', help = 'Api IP', default = '127.0.0.1')
@click.option('--port', '-p', help = 'Api port', default = 8000)
@click.argument('user_id', type=click.INT)
def get_user(user_id, host = '127.0.0.1', port = 8000):
	req = requests.get(f'http://{host}:{port}/users/{user_id}')
	print(req.text)

@cli.command()
@click.option('--host', '-h', help = 'Api IP', default = '127.0.0.1')
@click.option('--port', '-p', help = 'Api port', default = 8000)
@click.argument('user_id', type=click.INT)
def get_snapshots(user_id, host = '127.0.0.1', port = 8000):
	req = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots')
	print(req.text)

@cli.command()
@click.option('--host', '-h', help = 'Api IP', default = '127.0.0.1')
@click.option('--port', '-p', help = 'Api port', default = 8000)
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type = click.INT)
def get_snapshot(user_id, snapshot_id, host = '127.0.0.1', port = 8000):
	req = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}')
	print(req.text)

@cli.command()
@click.option('--host', '-h', help = 'Api IP', default = '127.0.0.1')
@click.option('--port', '-p', help = 'Api port', default = 8000)
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type = click.INT)
@click.argument('result', type = click.STRING)
def get_result(user_id, snapshot_id, result, host = '127.0.0.1', port = 8000):
	req = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result}')
	print(req.text)


if __name__ == '__main__':
	cli()

