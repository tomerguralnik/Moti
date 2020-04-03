from .connection import Connection
import socket


class Listener:

    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.sock = socket.socket()
        if reuseaddr:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def __repr__(self):
        port = self.port
        host = self.host
        backlog = self.backlog
        reuseaddr = self.reuseaddr
        return f'{self.__class__.__name__}\
                ({port=}, {host=!r}, {backlog=}, {reuseaddr=})'

    def start(self):
        self.sock.listen(self.backlog)

    def stop(self):
        self.sock.close()

    def accept(self):
        conn, addr = self.sock.accept()
        return Connection(conn, addr)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, excption, error, traceback):
        self.stop()
