from struct import pack, unpack

class Connection:
    """
    Connection is a simplification of socket for the purposes of
    the client-server connection
    """
    def __init__(self, sock, addr = ('127.0.0.1', 8000)):
        """
        :param sock: a socket
        :type sock: socket.socket
        :param addr: an adress to send exclusive messages to (host, port)
        :type addr: tuple
        """
        self.sock = sock
        self.addr = addr

    def __repr__(self):
        my_sock = ':'.join([str(i) for i in self.sock.getsockname()])
        con_sock = ':'.join([str(i) for i in self.sock.getpeername()])
        return f'<Connection from {my_sock} to {con_sock}>'

    def send(self, data):
        """
        :param data: data to send
        :type data: bytes
        """
        self.sock.sendall(data)

    def receive(self, size):
        """
        Receive a message of size exactly size

        :param size: size of expected message
        :type size: int
        """
        message = b''
        while len(message) < size:
            try:
                t = self.sock.recv(size - len(message))
                if t:
                    message += t
                else:
                    raise Exception('connection lost')
            except Exception:
                raise Exception('connection lost')
        return message

    def send_message(self, message):
        """
        Send a message and it's length in the beggining

        :param message: a message to send
        :type message: str
        """
        length = pack('I', len(message))
        message = length + message
        self.send(message)

    def send_message_to_addr(self, message):
        """
        Send a message and it's length in the beggining to self.addr

        :param message: a message to send
        :type message: str
        """
        length = pack('I', len(message))
        message = length + message
        self.sendto(message, self.addr)

    def receive_message(self):
        """
        Receive one message (length, message) and return message
        """
        try:
            length = unpack('I', self.receive(4))[0]
            message = self.receive(length)
        except Exception as e:
            raise e
        return message

    def close(self):
        """
        Close the socket, hence the conection
        """
        self.sock.close()

    def __enter__(self):
        return self

    def sendto(self, message, addr):
        """
        :param message: a messsage to send
        :type message: bytes
        :param addr: address to send the message to
        :type addr: tuple
        """
        self.sock.sendto(message, addr)

    def connect(host, port):
        """
        Create a Connection to (host, port) 

        :param host: ip 
        :type host: str
        :param port: port 
        :type port: int
        """
        import socket
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)