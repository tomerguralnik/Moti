import socket
import click
import datetime
from .thought import Thought
from .utils import Connection
from .cli import cli
from .utils import Reader
from .protocol import Hello, Config, Snapshot

@cli.command()
@click.option('--address', prompt='Adress', help='Adress of server')
@click.option('--user', prompt='user', help='User id of sender')
@click.option('--thought', prompt='thought', help='The thought')
def upload_thought(address, user, thought):
    thought = Thought(int(user), datetime.datetime.now(), thought)
    message = thought.serialize()
    address = address.split(':')
    address = (address[0], int(address[1]))
    sender = socket.socket()
    sender.connect(address)
    conn = Connection(sender)
    conn.send(message)
    conn.close()
    print('done')


@cli.command()
@click.option('--address', prompt='Address', help='Address of server')
@click.option('--snapshots', prompt='snapshots', help='User id of snapshot')
#@click.option('--thought', prompt='num', help='Number of snapshots to send')
def run_client(address, snapshots):
    address = address.split(':')
    address = (address[0], int(address[1]))
    sender = socket.socket()
    sender.connect(address)
    conn = Connection(sender)
    reader = Reader(snapshots)
    hello = Hello(reader.user_id, reader.user_name, datetime.datetime.strptime(reader.birth_date,'%Y-%m-%d %H:%M:%S'), reader.gender)
    for snapshot in reader:
        conn.send_message(hello.serialize())
        print('sent hello')
        config = Config.deserialize(conn.receive_message())
        print('got config')
        conn.send_message(snapshot.serialize(['translation','color_image']))
        print('done sanpshot')
    print('done')
    conn.close()


if __name__ == '__main__':
    cli.main()
