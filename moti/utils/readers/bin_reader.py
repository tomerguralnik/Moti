from pathlib import Path
from struct import unpack
from datetime import datetime

def read_string(message):
    point = 0
    x = yield
    while point < len(message):
        x = yield message[point: point + x]
        point += x

class BinReader:

    def __init__(self, path):
        path = Path(path)
        self.file = open(path, 'rb')

    def get_user(self):
        try:
            ret = {'user_id' : unpack('L', self.file.read(8))[0]}
            user_len = unpack('I', self.file.read(4))[0]
            ret['user_name'] = self.file.read(user_len).decode()
            ret['birth_date'] = datetime.fromtimestamp(unpack('I', self.file.read(4))[0])\
                                        .strftime('%Y-%m-%d %H:%M:%S')
            ret['gender'] = self.file.read(1).decode()
            return ret
        except Exception as e:
            print("bin_get_user failed", e)
            raise e

    def get_snapshot(self):
        try:
            ret = {'timestamp' : unpack('L', self.file.read(8))[0]}
            translation = unpack('ddd', self.file.read(24))
            ret['translation'] = {'x': translation[0],
                                  'y': translation[1],
                                  'z': translation[2]}
            rotation = unpack('d' * 4, self.file.read(32))
            ret['rotation'] = {'x': rotation[0],
                               'y': rotation[1],
                               'z': rotation[2],
                               'w': rotation[3]}
            color_height = unpack('I', self.file.read(4))[0]
            color_width = unpack('I', self.file.read(4))[0]
            color_image =[unpack('BBB', self.file.read(3)) for i in range(color_width * color_height)]
            ret['color_image'] =  ReaderImage(color_height, color_width, color_image, 'BBB')
            depth_height = unpack('I', self.file.read(4))[0]
            depth_width = unpack('I', self.file.read(4))[0]
            depth_image = [unpack('f', self.file.read(4))[0] for i in range(depth_width * depth_height)]
            ret['depth_image'] = ReaderImage(depth_height, depth_width, depth_image, 'f')
            feelings = unpack('f' * 4, self.file.read(16))
            ret['feelings'] = {'hunger': feelings[0],
                               'thirst': feelings[1],
                               'exhaustion': feelings[2],
                               'happiness': feelings[3]}
            return ret
        except Exception as e:
            print("bin_get_snapshot failed", e)
            raise e

'''
    def __next__(self):
        try:
            timestamp = int(unpack('L', self.file.read(8))[0]/1000)
            #timestamp = datetime.fromtimestamp(timestamp/1000)\
            #    .strftime('%Y-%m-%d %H:%M:%S.%f')
            translation = unpack('ddd', self.file.read(24))
            rotation = unpack('d' * 4, self.file.read(32))
            color_height = unpack('I', self.file.read(4))[0]
            color_width = unpack('I', self.file.read(4))[0]
            color_image = Snapshot.Image.deserialize(self.file.read(color_height * color_width * 3)\
                                                        ,color_height, color_width, 'color')
            depth_height = unpack('I', self.file.read(4))[0]
            depth_width = unpack('I', self.file.read(4))[0]
            depth_image = Snapshot.Image.deserialize(self.file.read(depth_height * depth_width * 4)\
                                                        ,depth_height, depth_width, 'depth')
            feelings = unpack('f' * 4, self.file.read(16))
            return Snapshot(timestamp, translation, rotation,
                            color_image, depth_image, feelings)
        except Exception:
            raise StopIteration()
'''


class ReaderImage:
    def __init__(self, height, width, image, fmt):
        self.height = height
        self.width = width
        self.image = image
        self.fmt = fmt
