from .connection import Connection
import socket


class Listener:
    """
    Listener is basically a socket that listens but when it accepts
    a connection it returns a Connection instead of socket
    """
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        """
        :param port: port
        :type port: int
        :param host: ip, defaults to '0.0.0.0'
        :type host: str(,optional)
        :param backlog: backlog for socket.listen, defaults to 1000
        :type backlog: int(,optional)
        :param reuseaddr: reuseaddr for sick.setsickopt, defaults to True
        :type reuseaddr: bool
        """
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.sock = socket.socket()
        if reuseaddr:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))


    def start(self):
        """
        Start listening fro connections
        """
        self.sock.listen(self.backlog)

    def stop(self):
        """
        Close the listening socket
        """
        self.sock.close()

    def accept(self):
        """
        Accept a connection

        :return: a Connection object representing the connection
        :rtype: Conneciton
        """
        conn, addr = self.sock.accept()
        return Connection(conn, addr)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, excption, error, traceback):
        self.stop()
