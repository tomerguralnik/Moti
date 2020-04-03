from struct import pack, unpack

class Connection:

    def __init__(self, sock, addr = '127.0.0.1:8000'):
        self.sock = sock
        self.addr = addr;

    def __repr__(self):
        my_sock = ':'.join([str(i) for i in self.sock.getsockname()])
        con_sock = ':'.join([str(i) for i in self.sock.getpeername()])
        return f'<Connection from {my_sock} to {con_sock}>'

    def send(self, data):
        self.sock.sendall(data)

    def receive(self, size):
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
        length = pack('I', len(message))
        message = length + message
        self.send(message)

    def send_message_to_addr(self, message):
        length = pack('I', len(message))
        message = length + message
        self.sendto(message, self.addr)

    def receive_message(self):
        try:
            length = unpack('I', self.receive(4))[0]
            message = self.receive(length)
        except Exception as e:
            raise e
        return message

    def close(self):
        self.sock.close()

    def __enter__(self):
        return self

    def sendto(self, message, addr):
        self.sock.sendto(message, addr)

    def connect(host, port):
        import socket
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)

    def __exit__(self, exception, error, traceback):
        self.close()
