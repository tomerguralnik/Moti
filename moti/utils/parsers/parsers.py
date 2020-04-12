from pathlib import Path
from PIL import Image
import json
import matplotlib.pyplot as plt
import numpy as np

def parse_color_image(snapshot, path):
    path = path / 'color_image.jpg'
    path.touch()
    height = snapshot.color_image.height
    width = snapshot.color_image.width
    image = Image.new('RGB', (height, width))
    image.putdata(snapshot.color_image.image)
    image.save(path)

parse_color_image.fields = ['color_image']

def parse_pose(snapshot, path):
    path = path/'pose.json'
    path.touch()
    fp = path.open('w')
    json.dump(snapshot.pose, fp)

parse_pose.fields = ['translation', 'rotation']

def parse_feelings(snapshot, path):
    path = path/'feelings.json'
    path.touch()
    fp = path.open('w')
    json.dump(snapshot.feelings, fp)

parse_feelings.fields = ['feelings']

def parse_depth_image(snapshot, path):
    path = path/'depth_image.jpg'
    image = np.reshape(from_tup(snapshot.depth_image.image), (-1, snapshot.depth_image.height))
    plt.imshow(image)
    plt.savefig(path)

parse_depth_image.fields = ['depth_image']

def from_tup(image):
    return [box[0] for box in image]