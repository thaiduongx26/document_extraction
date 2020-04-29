import logging.config

from . import sensor, ai, settings
from .settings import settings, enable_debug, Folder
from .utils import *

logging.config.dictConfig(settings['logging'])
