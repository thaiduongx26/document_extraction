import logging.config

from . import sensor, settings
from .settings import settings, enable_debug, Folder
from .utils import *

print("settings: ", settings)
print("settings loggings: ", settings['logging'])

# logging.config.dictConfig(settings['logging'])
