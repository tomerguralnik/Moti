import socket
import click
import datetime
from .thought import Thought
from .utils import Connection
from .cli import client
from .utils import Reader
from .utils import Hello, Config, Snapshot
from .utils import Config_handler
import logging
logging.basicConfig(format = '%(levelname).1s %(asctime)s %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('client')
logger.setLevel(logging.INFO)


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
                                  
                           

@client.command()
@click.option('--host', '-h', help='Address of server', default = '127.0.0.1')
@click.option('--port', '-p', help='User id of snapshot', default = '8000')
@click.option('--path', help='Number of snapshots to send', default = 'sample.mind.gz')
@click.option('--config', '-c', help = 'Config file', default = None)
def upload_sample(host = '127.0.0.1', port = '8000', path = 'sample.mind.gz', config = None):
    if config:
        config = Config_handler(config, 'client')
        host = config.host
        port = config.port
        path = config.path
    address = (host, int(port))
    sender = socket.socket()
    sender.connect(address)
    conn = Connection(sender)
    reader = Reader(path, 'proto_reader')
    hello = Hello(reader.user_id, reader.user_name, datetime.datetime.strptime(reader.birth_date,'%Y-%m-%d %H:%M:%S'), reader.gender)
    for snapshot in reader:
        serv_snap = reader_to_server(snapshot)
        conn.send_message(hello.serialize())
        logger.info('sent hello')
        config = Config.deserialize(conn.receive_message())
        logger.info('got config')
        conn.send_message(serv_snap.serialize(config.fields))
        logger.info('done snapshot')
    logger.info('done')
    conn.close()


if __name__ == '__main__':
    client()
