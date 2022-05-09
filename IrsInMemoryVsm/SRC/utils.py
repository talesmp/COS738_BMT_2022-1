import logging
import logging.config
from configparser import ConfigParser

PROGRAM_CONFIG_FILENAME = 'config.ini'
LOGGING_CONFIG_FILENAME = 'logging.ini'

def init_irs(name):
    config = read_config(name)
    logger = create_logger(name)
    return config, logger

def read_config(name):
    config = ConfigParser()
    config.read(PROGRAM_CONFIG_FILENAME)
    return config[name]

def create_logger(name):
    logging.config.fileConfig(LOGGING_CONFIG_FILENAME)
    logger = logging.getLogger(name)
    return logger

