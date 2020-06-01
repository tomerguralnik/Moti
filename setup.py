from setuptools import setup, find_packages


setup(
    name = 'moti',
    version = '1.0.0',
    author = 'Tomer Guralnik',
    description = 'Moti!',
    packages = find_packages(),
    install_requires = ['click', 'flask', 'Werkzeug', 'pika', 'PyYaml', 'pynpm', 
    	'pymongo', 'protobuf', 'Pillow', 'numpy', 'matplotlib', 'furl', 'Flask', 'Flask-Cors', 'flake8']
)