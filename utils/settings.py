from pathlib import Path

import logging

logger = logging.getLogger(__name__)


def load_settings(config_file='data/config/config.yaml') -> dict:
    """Load settings from config file, if the config file not exist, load the default config file.
    :param config_file: path to the config file.
    :return: the loaded configuration.
    """
    logger.info(f'Loading config from "{config_file}"')

    try:
        if not Path(config_file).exists():
            config_file = 'config/config.yaml'
            logger.warning('Config file not found. Using default value.')
        with open(config_file, 'r') as f:
            import yaml
            return yaml.safe_load(f.read())
    except BaseException as e:
        logger.exception(f'Unable load settings due to {e}')
        raise


settings = load_settings()

try:
    enable_debug = settings['debugging']['enable']
except BaseException:
    pass
enable_debug = True



class Folder:
    input = 'E:\\document_reading/input'
    working = 'E:\\document_reading/working'
    output = 'E:\\document_reading/output'
    log = 'E:\\document_reading/log'
    config = 'E:\\document_reading/config'
