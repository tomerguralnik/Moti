import threading
from pathlib import Path
from struct import unpack
import click
from .cli import cli
from .utils import Listener
from .thought import Thought
from .protocol import Hello, Config, Snapshot
from .utils import read_string, Parser
from PIL import Image
import json
from datetime import datetime
from functools import reduce
parser = Parser()

def reverse(tup):
    a,b,c = tup
    return (a, b, c)

@cli.command()
@click.option('--address', prompt='Adress', help='Adress of server')
@click.option('--data', prompt='data dict', help='The path to data dictionary')
def run_server(address, data):
    address = address.split(':')
    host, port = address[0], int(address[1])
    server = Listener(port, host)
    server.start()
    p = Path(data)
    if p.is_file():
        raise Exception('data is a file and not a directory')
    while True:
        client = server.accept()
        t = threading.Thread(target=session_handler, args=(client, p))
        t.start()
    server.stop()


def session_handler(client, path):
    while(True):
        fields = parser.parsers.keys()
        lock = threading.Lock()
        try:
            hi_message = client.receive_message()
        except Exception:
            print("bad hello message")
            return
        try:
            hello = Hello.deserialize(hi_message)
        except Exception as e:
            print("Hello:", e)
            return
        print('got hello')
        config = Config(fields)
        client.send_message_to_addr(config.serialize())
        print('sent config')
        try:
            snap_message = client.receive_message()
        except Exception:
            print("bad snapshot")
            return
        try:
            snapshot = Snapshot.deserialize(snap_message)
        except Exception as e:
            print("Snapshot:", e)
            return
        print('got snapshot')
        lock.acquire()
        p = path / f'{hello.user_id}'
        p.mkdir(exist_ok=True)
        p = p / f"{datetime.fromtimestamp(snapshot.timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f')}"
        p.mkdir(exist_ok=True)
        parser.parse(fields ,snapshot, p)
        lock.release()
        print('done')


@parser.wrap('translation')
def parse_translation(snapshot, path):
    path = path / 'translation.json'
    translation = {"x": snapshot.translation[0],
                   "y": snapshot.translation[1],
                   "z": snapshot.translation[2]}
    path.touch()
    fp = path.open('w')
    json.dump(translation, fp)


@parser.wrap('color_image')
def parse_color_image(snapshot, path):
    path = path / 'color_image.jpg'
    path.touch()
    height = len(snapshot.color_image.image)
    width = 0 if height == 0 else len(snapshot.color_image.image[0])
    image = Image.new('RGB', (height, width))
    #image.putdata([reverse(i) for i in reduce(lambda a, b: a + b, snapshot.color_image.image)])
    image.putdata(reduce(lambda a, b: a + b, snapshot.color_image.image))
    image.save(path)


if __name__ == '__main__':
    cli.main()
