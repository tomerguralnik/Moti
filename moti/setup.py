from setuptools import setup, find_packages

setup(
    name = 'Project',
    version = '1.0.0',
    author = 'Tomer Guralnik',
    description = 'Project',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov']
)
