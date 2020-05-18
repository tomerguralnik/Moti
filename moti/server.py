import threading
from pathlib import Path
import click
from .utils import Listener
from .utils import Hello, Config, Snapshot
from .utils import Parser
from .utils import Config_handler
from .utils import Publisher
from furl import furl
parser = Parser()

@click.group()
def server():
    pass

def reverse(tup):
    a,b,c = tup
    return (c, b, a)

def run_server(publish, host = '127.0.0.1', port = 8000):
    server = Listener(int(port), host)
    server.start()
    while True:
        client = server.accept()
        t = threading.Thread(target=session_handler, args=(client, publish))
        t.start()
    server.stop()


def session_handler(client, publish):
    while(True):
        fields = parser.fields
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
        print(fields)
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
        snapshot.user = hello.as_dict
        publish(snapshot)
        print('done')

@server.command(name = 'run-server')
@click.option('--host', '-h', help='Address of server', default = '127.0.0.1')
@click.option('--port', '-p', help='User id of snapshot', default = '8000')
@click.option('--config', '-c', help = 'Config file', default = None)
@click.argument('queue', nargs = -1, type = click.STRING)
def cli_run_server(queue, host = '127.0.0.1', port = 8000, config = None):
    if config:
        config = Config_handler(config, 'server')
        host = config.host
        port = config.port
        queue = config.queue
    else:
        queue = queue[0]
    queue = furl(queue)
    queue.scheme = queue.scheme + '_server'
    data_dict = Path(__file__).parent.parent.absolute()/'data'
    publisher = Publisher(parser.generate_queues(), str(queue), path = data_dict)
    run_server(publisher, host, port)

if __name__ == '__main__':
    server()
