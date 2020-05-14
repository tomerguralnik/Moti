from pathlib import Path
from PIL import Image
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def parse_color_image(snapshot, path):
    print('color_image')
    snapshot = Path(snapshot.decode('ascii'))
    with snapshot.open() as snap:
        snapshot = json.load(snap)
        image = snapshot['color_image']
    color_image = np.load(image['image'])
    path = path / str(snapshot['user']['user_id'])
    path.mkdir(exist_ok = True)
    path = path / datetime.fromtimestamp(snapshot['timestamp']/1000).strftime('%Y-%m-%d_%H-%M-%S.%f')
    path.mkdir(exist_ok = True)
    path = path / 'color_image.jpg'
    path.touch()
    height = image['height']
    width = image['width']
    image = Image.new('RGB', (height, width))
    image.putdata([tuple(pixel) for pixel in color_image.tolist()])
    image.save(path)
    return json.dumps({'user': snapshot['user'],
                       'timestamp': snapshot['timestamp'],
                       'color_image': str(path.absolute())})

parse_color_image.fields = ['color_image']

def parse_pose(snapshot, path):
    print('pose')
    snapshot = Path(snapshot.decode('ascii'))
    with snapshot.open() as snap:
        snapshot = json.load(snap)
    return json.dumps({'user': snapshot['user'],
                       'timestamp': snapshot['timestamp'],
                       'pose': snapshot['pose']})

parse_pose.fields = ['pose']

def parse_feelings(snapshot, path):
    print('feelings')
    snapshot = Path(snapshot.decode('ascii'))
    with snapshot.open() as snap:
        snapshot = json.load(snap)
    return json.dumps({'user': snapshot['user'], 
                       'timestamp': snapshot['timestamp'],
                       'feelings': snapshot['feelings']})

parse_feelings.fields = ['feelings']

def parse_depth_image(snapshot, path):
    print('depth_image')
    snapshot = Path(snapshot.decode('ascii'))
    with snapshot.open() as snap:
        snapshot = json.load(snap)
        image = snapshot['depth_image']
    depth_image = np.load(image['image'])
    path = path / str(snapshot['user']['user_id'])
    path.mkdir(exist_ok = True)
    path = path / datetime.fromtimestamp(snapshot['timestamp']/1000).strftime('%Y-%m-%d_%H-%M-%S.%f')
    path.mkdir(exist_ok = True)
    path = path/'depth_image.jpg'
    image = np.reshape(depth_image, (-1, image['height']))
    plt.imshow(image)
    plt.savefig(path)
    return json.dumps({'user': snapshot['user'], 
                       'timestamp': snapshot['timestamp'],
                       'depth_image': str(path.absolute())})

parse_depth_image.fields = ['depth_image']

def from_tup(image):
    return [box[0] for box in image]
