from struct import pack, unpack
import datetime


class Thought:

    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'{self.__class__.__name__}(user_id={self.user_id},\
                timestamp={self.timestamp!r}, thought={self.thought!r})'

    def __str__(self):
        date = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return f'[{date}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.user_id, self.timestamp, self.thought) ==\
                    (other.user_id, other.timestamp, other.thought)
        return False

    def serialize(self):
        message = pack('L', self.user_id)
        message += pack('L', int(self.timestamp.timestamp()))
        message += pack('I', len(self.thought.encode()))
        message += self.thought.encode()
        return message

    def deserialize(data):
        try:
            user_id = unpack('L', data[:8])[0]
            timestamp = unpack('L', data[8:16])[0]
            m_len = unpack('I', data[16:20])[0]
            thought = data[20:].decode()
            if m_len != len(thought):
                raise Exception('invalid data')
            return Thought(user_id,
                           datetime.datetime.fromtimestamp(timestamp), thought)
        except Exception:
            raise Exception('invalid data')
