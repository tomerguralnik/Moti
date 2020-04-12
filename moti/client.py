import socket
import click
import datetime
from .thought import Thought
from .utils import Connection
from .cli import cli
from .utils import Reader
from .utils import Hello, Config, Snapshot


def reader_to_server(snapshot):
    timestamp = snapshot.timestamp
    translation = snapshot.translation
    rotation = snapshot.rotation
    color_image = snapshot.color_image
    color_image = Snapshot.Image(color_image.height, color_image.width,
                                color_image.image, color_image.fmt)
    depth_image = snapshot.depth_image
    depth_image = Snapshot.Image(depth_image.height, depth_image.width,
                                depth_image.image, depth_image.fmt)
    feelings = snapshot.feelings
    return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)  
                                  
                           

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
    reader = Reader(snapshots, 'proto_reader')
    hello = Hello(reader.user_id, reader.user_name, datetime.datetime.strptime(reader.birth_date,'%Y-%m-%d %H:%M:%S'), reader.gender)
    for snapshot in reader:
        serv_snap = reader_to_server(snapshot)
        conn.send_message(hello.serialize())
        print('sent hello')
        config = Config.deserialize(conn.receive_message())
        print('got config')
        conn.send_message(serv_snap.serialize(config.fields))
        print('done snapshot')
    print('done')
    conn.close()


if __name__ == '__main__':
    cli.main()
