from struct import pack, unpack, calcsize
from datetime import datetime
from functools import reduce
import numpy

def read_string(message):
    point = 0
    p_2 = 0
    x = yield
    while point < len(message):
        p_2 += x
        x = yield message[point: point + x]
        point = p_2



class Hello:

    def __init__(self, user_id, user_name, birth_date, gender):
        self.user_id = user_id
        self.user_name = user_name
        self.birth_date = birth_date
        self.gender = gender
        self.as_dict = {'user_id': user_id,
                        'user_name' : user_name,
                        'birth_date' : int(birth_date.timestamp()),
                        'gender' : gender}

    def serialize(self):
        message = b''
        message += pack('L', self.user_id)
        message += pack('I', len(self.user_name))
        message += self.user_name.encode()
        message += pack('I', int(self.birth_date.timestamp()))
        message += self.gender.encode()
        return message

    def deserialize(message):
        try:
            reader = read_string(message)
            next(reader)
            user_id = unpack('L', reader.send(8))[0]
            user_name_l = unpack('I', reader.send(4))[0]
            user_name = reader.send(user_name_l).decode()
            birth_date = datetime.fromtimestamp(unpack('I', reader.send(4))[0])
            gender = reader.send(1).decode()
        except Exception:
            raise Exception("Message has wrong format 1")
        try:
            a = reader.send(1)
        except StopIteration:
            return Hello(user_id, user_name, birth_date, gender)
        raise Exception("Message has wrong format 2")

    def __str__(self):
        u_id = self.user_id
        u_nm = self.user_name
        b_dt = self.birth_date.strftime('%Y-%m-%d %H:%M:%S')
        gender = self.gender
        return f'{u_id}, {u_nm}, Born {b_dt}, {gender=}'

    def __repr__(self):
        return f'Hello({self.user_id}, {self.user_name},\
                {self.birth_date}, {self.gender})'


class Config:

    def __init__(self, fields):
        self.fields = fields

    def serialize(self):
        message = b''
        message += pack('I', len(self.fields))
        for field in self.fields:
            message += pack('I', len(field))
            message += field.encode()
        return message

    def deserialize(message):
        reader = read_string(message)
        next(reader)
        fields = []
        try:
            num_fields = unpack('I', reader.send(4))[0]
            for i in range(num_fields):
                field_len = unpack('I', reader.send(4))[0]
                field = reader.send(field_len).decode()
                fields.append(field)
        except Exception as e:
            raise e
        try:
            a = reader.send(1)
            if a == b'\x00':
                return Config(fields)
        except StopIteration:
            return Config(fields)
        raise Exception("Message has wrong format 2")

    def __repr__(self):
        return f'Config({self.fields})'

    def __str__(self):
        fields = ', '.join(self.fields)
        return f'Supported fields: {fields}'


class Snapshot:

    class Image:

        def __init__(self, height, width, image, fmt):
            self.height = height
            self.width = width
            self.image = image
            self.fmt =  fmt

        def compactify(self, path, timestamp):
            path = path / (self.fmt + 'TIME'+ datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d_%H-%M-%S.%f') + '.bin')
            fp = path.open('wb+')
            for box in self.image:
                fp.write(pack(self.fmt, *box))
            fp.close()
            return {'height' : self.height,
                    'width' : self.width,
                    'image' : str(path),
                    'fmt' : self.fmt}

        def serialize(self):
            try:
                size = calcsize(self.fmt)
            except:
                raise Exception(f"{self.fmt} isn't a supported format")
            message = b''
            message += pack('I', self.width)
            message += pack('I', self.height)
            image = [pack(self.fmt, *box) for box in self.image]
            message += b''.join(image)
            return message

        def deserialize(message, height, width, fmt):
            try:
                size = calcsize(fmt)
            except:
                raise Exception(f"{fmt} isn't a supported format")
            reader = read_string(message)
            next(reader)
            image = [0  for i in range(height * width)]
            for i in range(height * width):
                image[i] = unpack(fmt, reader.send(size))
            return Snapshot.Image(height, width, image, fmt)


    def __init__(self, timestamp, translation,
                 rotation, color_image, depth_image, feelings):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings
        self.pose = {'translation': self.translation, 
                     'rotation': self.rotation}

    def serialize(self, fields):
        translation = (self.translation['x'],
                       self.translation['y'],
                       self.translation['z']) \
                       if 'translation' in fields else (0, 0, 0)
        rotation = (self.rotation['x'],
                    self.rotation['y'],
                    self.rotation['z'],
                    self.rotation['w']) \
                     if 'rotation' in fields else (0, 0, 0, 0)
        color_image = self.color_image if \
            'color_image' in fields else Snapshot.Image(0, 0, [], 'BBB')
        depth_image = self.depth_image if \
            'depth_image' in fields else Snapshot.Image(0, 0, [], 'f')
        feelings = (self.feelings['hunger'],
                    self.feelings['thirst'],
                    self.feelings['exhaustion'],
                    self.feelings['happiness'])\
                    if 'feelings' in fields else (0, 0, 0, 0)
        message = b''
        message += pack('L', self.timestamp)
        message += pack('ddd', *translation)
        message += pack('dddd', *rotation)
        message += color_image.serialize()
        message += depth_image.serialize()
        message += pack('ffff', *feelings)
        return message

    def deserialize(message):
        reader = read_string(message)
        next(reader)
        timestamp = unpack('L', reader.send(8))[0]
        translation = unpack('ddd', reader.send(24))
        translation = {'x': translation[0],
                      'y': translation[1],
                      'z': translation[2]}
        rotation = unpack('dddd', reader.send(32))
        rotation = {'x': rotation[0],
                    'y': rotation[1],
                    'z': rotation[2],
                    'w': rotation[3]}
        height = unpack('I', reader.send(4))[0]
        width = unpack('I', reader.send(4))[0]
        color_image = Snapshot.Image.deserialize(
            reader.send(width * height * 3), height, width, 'BBB')
        height = unpack('I', reader.send(4))[0]
        width = unpack('I', reader.send(4))[0]
        depth_image = Snapshot.Image.deserialize(
                                reader.send(width * height * 4), height, width, 'f')
        feelings = unpack('ffff', reader.send(16))
        feelings = {'hunger': feelings[0],
                    'thirst': feelings[1],
                    'exhaustion': feelings[2],
                    'happiness': feelings[3]}
        return Snapshot(timestamp, translation, rotation,
                        color_image, depth_image, feelings)

    def compactify(self, path):
        return {'timestamp' : self.timestamp,
                'translation': self.translation,
                'rotation' : self.rotation,
                'color_image' : self.color_image.compactify(path, self.timestamp),
                'depth_image' : self.depth_image.compactify(path, self.timestamp),
                'feelings' : self.feelings,
                'pose' : self.pose}

    def __repr__(self):
        return f'''Time: {self.timestamp}, Translation: {self.translation}
Rotation: {self.rotation}
Color Image: {self.color_image}
Depth Image: {self.depth_image}
{self.feelings}'''
