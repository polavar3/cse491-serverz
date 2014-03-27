# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the fiile 'root.py'
from .root import RootDirectory
from . import html, image

def create_publisher():
    p = Publisher(RootDirectory(), display_exceptions='plain')
    p.is_thread_safe = True
    return p

def setup():
    html.init_templates()

    some_data = open('imageapp/lfc.jpg', 'rb').read()
    image.add_image('imageapp/lfc.jpg', some_data)

def teardown():
    pass
