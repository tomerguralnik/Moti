from pathlib import Path
from struct import unpack
from datetime import datetime
import gzip
from . import cortex_pb2
genders = {0: 'm', 1:'f', 2: 'o'}
class ProtoReader:

	def __init__(self, path):
		self.file = gzip.open(Path(path), 'rb')

	def get_user(self):
		try: 
			length = unpack('I', self.file.read(4))[0]
			user = cortex_pb2.User()
			user.ParseFromString(self.file.read(length))
			print(user)
			ret = {'user_id' : user.user_id}
			ret['user_name'] = user.username
			ret['birth_date'] = datetime.fromtimestamp(user.birthday)\
								.strftime('%Y-%m-%d %H:%M:%S')
			ret['gender'] = genders[user.gender]
			return ret
		except Exception as e:
			print("get_user failed", e)
			raise e

	def get_snapshot(self):
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
			print("get_sanpshot failed", e)
			raise e

def convert_to_image(protoimage, fmt):
	return ReaderImage(protoimage.height, protoimage.width, data_to_image(protoimage.data, len(fmt)), fmt)


class ReaderImage:
    def __init__(self, height, width, image, fmt):
        self.height = height
        self.width = width
        self.image = image
        self.fmt = fmt


def data_to_image(data, length):
	return [tuple([data[j] for j in range(i * length, (i+1) * length)])
			 for i in range(len(data)//length)]

		