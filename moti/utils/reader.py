from pathlib import Path
from struct import unpack
from datetime import datetime
from moti.protocol import Snapshot


class Reader:

    def __init__(self, path):
        path = Path(path)
        self.file = open(path, 'rb')
        self.user_id = unpack('L', self.file.read(8))[0]
        user_len = unpack('I', self.file.read(4))[0]
        self.user_name = self.file.read(user_len).decode()
        birth = unpack('I', self.file.read(4))[0]
        self.birth_date = datetime.fromtimestamp(birth)\
            .strftime('%Y-%m-%d %H:%M:%S')
        self.gender = self.file.read(1).decode()

    def __iter__(self):
        return self

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