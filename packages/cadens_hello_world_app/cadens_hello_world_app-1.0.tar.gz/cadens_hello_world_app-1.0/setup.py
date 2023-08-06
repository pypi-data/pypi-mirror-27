import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'cadens_hello_world_app',
    packages = ['cadens_hello_world_app'], # this must be the same as the name above
    version = '1.0',
    description = 'Prints Hello World',
    keywords = 'pythonA hello world', #Add any keyword related to your package
)

