from ai.interfaces import ai_interface

import logging

logger = logging.getLogger(__name__)


def initialize_ai_model():
    logger.info("Initializing ai model")

    # Initialize AI model here
    model = ai_interface.AI_Interface(config_dir='ai/storage')
    model.load_data(load_folder='models')

    return model
