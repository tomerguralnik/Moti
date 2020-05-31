from pathlib import Path
from PIL import Image
import json
import matplotlib.pyplot as plt
import numpy as np
from struct import pack, unpack
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D

include = 1

def parse_color_image(snapshot, path):
    """
    Saves the color image from the snapshot to the directory path as a jpg
    and returns it toghther with some user information

    :param snaphsot: a path to a json file containing snapshot information
        as saved by rabbitmq_server_publisher
    :type snapshot: str
    :param path: a path to a directory for the parsers to save their files to
    :type path: str 
    :return: json string that contains a dictionary with user information,
        timestamp, and path to the color image
    :rtype: json str
    """
    print('color_image')
    snapshot = Path(snapshot.decode('ascii'))
    with snapshot.open() as snap:
        snapshot = json.load(snap)
        image = snapshot['color_image']
    color_image_bin = open(image['image'], 'rb').read()
    color_image = [unpack('BBB', color_image_bin[i*3 : i*3 + 3]) for i in range(len(color_image_bin)//3)]
    color_image = np.array(color_image)
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
    """
    Saves a 3d representation of the translation from snapshot, returns
    normal pose representation toghether with a path to the 3d representation
    and some user data

    :param snaphsot: a path to a json file containing snapshot information
        as saved by rabbitmq_server_publisher
    :type snapshot: str
    :param path: a path to a directory for the parsers to save their files to
    :type path: str 
    :return: json string that contains a dictionary with user information,
        timestamp, and pose, pose contains a path to 3d representation of translation
    :rtype: json str
    """
    print('pose')
    snapshot = Path(snapshot.decode('ascii'))
    with snapshot.open() as snap:
        snapshot = json.load(snap)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set(xlim = (-5, 5), ylim = (-5, 5), zlim = (-5, 5))
    ax.plot([snapshot['pose']['translation']['x']],[snapshot['pose']['translation']['y']],[snapshot['pose']['translation']['z']], marker = 'o')
    path = path / str(snapshot['user']['user_id'])
    path.mkdir(exist_ok = True)
    path = path / datetime.fromtimestamp(snapshot['timestamp']/1000).strftime('%Y-%m-%d_%H-%M-%S.%f')
    path.mkdir(exist_ok = True)
    path = path/'translation.jpg'
    fig.savefig(path)
    plt.close(fig)
    snapshot['pose']['translation_picture'] = str(path.absolute()) 
    return json.dumps({'user': snapshot['user'],
                       'timestamp': snapshot['timestamp'],
                       'pose': snapshot['pose']})

parse_pose.fields = ['pose']

def parse_feelings(snapshot, path):
    """
    Returns the feelings as they are in snapshot toghether with some user
    information

    :param snaphsot: a path to a json file containing snapshot information
        as saved by rabbitmq_server_publisher
    :type snapshot: str
    :param path: a path to a directory for the parsers to save their files to
    :type path: str
    :return: json string that contains a dictionary with user information,
        timestamp, and feelings
    :rtype: json str
    """
    print('feelings')
    snapshot = Path(snapshot.decode('ascii'))
    with snapshot.open() as snap:
        snapshot = json.load(snap)
    return json.dumps({'user': snapshot['user'], 
                       'timestamp': snapshot['timestamp'],
                       'feelings': snapshot['feelings']})

parse_feelings.fields = ['feelings']

def parse_depth_image(snapshot, path):
    """
    Saves the depth image from the snapshot to the directory path as a jpg
    and returns it toghther with some user information

    :param snaphsot: a path to a json file containing snapshot information
        as saved by rabbitmq_server_publisher
    :type snapshot: str
    :param path: a path to a directory for the parsers to save their files to
    :type path: str
    :return: json string that contains a dictionary with user information,
        timestamp, and path to the depth image
    :rtype: json str
    """
    print('depth_image')
    snapshot = Path(snapshot.decode('ascii'))
    with snapshot.open() as snap:
        snapshot = json.load(snap)
        image = snapshot['depth_image']
    depth_image_bin = open(image['image'], 'rb').read()
    depth_image = [unpack('f', depth_image_bin[i*4 : i*4 + 4]) for i in range(len(depth_image_bin)//4)]
    depth_image = np.array(depth_image)
    path = path / str(snapshot['user']['user_id'])
    path.mkdir(exist_ok = True)
    path = path / datetime.fromtimestamp(snapshot['timestamp']/1000).strftime('%Y-%m-%d_%H-%M-%S.%f')
    path.mkdir(exist_ok = True)
    path = path/'depth_image.jpg'
    image = np.reshape(depth_image, (-1, image['height']))
    fig, ax = plt.subplots()
    ax.imshow(image)
    fig.savefig(path)
    plt.close(fig)
    return json.dumps({'user': snapshot['user'], 
                       'timestamp': snapshot['timestamp'],
                       'depth_image': str(path.absolute())})

parse_depth_image.fields = ['depth_image']