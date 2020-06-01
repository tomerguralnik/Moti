from pathlib import Path
from struct import unpack
from datetime import datetime
import struct
import gzip
from . import cortex_pb2
genders = {0: 'm', 1:'f', 2: 'o'}
class ProtoReader:
    """
    A reader that reads using protobufs and assumes the format is like
    the one in the project specification
    """
    def __init__(self, path):
        """
        :param path: path to smaple file
        :type path: str
        """
        self.file = gzip.open(Path(path), 'rb')

    def get_user(self):
        """
        Get the users information
        """
        try: 
            test = self.file.read(4)
            length = unpack('I', test)[0]
            user = cortex_pb2.User()
            user.ParseFromString(self.file.read(length))
            ret = {'user_id' : user.user_id}
            ret['user_name'] = user.username
            ret['birth_date'] = datetime.fromtimestamp(user.birthday)\
                                .strftime('%Y-%m-%d %H:%M:%S')
            ret['gender'] = genders[user.gender]
            return ret
        except Exception as e:
            print("get_user failed", e)
            print("test", test)
            raise e

    def get_snapshot(self):
        """
        Get the snapshot's information
        """
        try:
            length = unpack('I', self.file.read(4))[0]
            snapshot = cortex_pb2.Snapshot()
            snapshot.ParseFromString(self.file.read(length))
            ret = {'timestamp': snapshot.datetime}
            ret['translation'] = {'x': snapshot.pose.translation.x,
                                  'y': snapshot.pose.translation.y,
                                  'z': snapshot.pose.translation.z}
            ret['rotation'] = {'x': snapshot.pose.rotation.x,
                               'y': snapshot.pose.rotation.y,
                               'z': snapshot.pose.rotation.z,
                               'w': snapshot.pose.rotation.w}
            ret['color_image'] = convert_to_image(snapshot.color_image, 'BBB')
            ret['depth_image'] = convert_to_image(snapshot.depth_image, 'f')
            ret['feelings'] = {'hunger': snapshot.feelings.hunger,
                               'exhaustion': snapshot.feelings.exhaustion,
                               'thirst': snapshot.feelings.thirst,
                               'happiness': snapshot.feelings.happiness}
            return ret
        except Exception as e:
            if isinstance(e, struct.error): 
                raise StopIteration
            print("get_sanpshot failed", e)
            raise e

def convert_to_image(protoimage, fmt):
    """
    :param protoimage: an image from protobuf
    :type protoimage: an image as defined in the protobuf
    :param fmt: the struct format of the image, for example: RGB would be 'BBB' 
    :type fmt: str
    :return: a reader image with proto image properties
    :rtype: ReaderImage
    """
    return ReaderImage(protoimage.height, protoimage.width, data_to_image(protoimage.data, len(fmt)), fmt)


class ReaderImage:
    """
    A more suitable format for images
    """
    def __init__(self, height, width, image, fmt):
        """
        :param height: the height of the image
        :type height: int
        :param width: the width of the image
        :type width: int
        :param image: the image in a flat list of tuples according to fmt
        :type image: list
        :param fmt: the struct format of the image, for example: RGB would be 'BBB' 
        :type fmt: str
        """
        self.height = height
        self.width = width
        self.image = image
        self.fmt = fmt


def data_to_image(data, length):
    """
    :param data: a protobuf image
    :type data: list
    :param length: the length of the struct format of image
    :type length: int
    :return: a flat list of tuples of lenght length
    :rtype: list
    """
    return [tuple([data[j] for j in range(i * length, (i+1) * length)])
             for i in range(len(data)//length)]

        
