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

enable_debug = False
try:
    enable_debug = settings['debugging']['enable']
except BaseException:
    pass


class Folder:
    input = 'data/input'
    working = 'data/working'
    output = 'data/output'
    log = 'data/log'
    config = 'data/config'
