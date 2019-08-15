import os
import yaml
import logging
import logging.handlers

from constants import Constants

LOG_DIR = os.path.join('logs')
config = None


def initialize_config(env, server_config):
    global config
    with open(server_config) as f:
        conf = yaml.full_load(f)
        config = conf[env]
    return config


def initialize_logger(logger_name=Constants.MICROSERVICE_NAME):
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    logger = logging.getLogger(logger_name)
    if config.get('log_debug'):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # file logger
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(LOG_DIR, "app.log"),
        mode='a',
        maxBytes=(1048576*5),
        backupCount=7,
        encoding=None,
        delay="true"
        )
    file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s] %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    if config.get('log_debug'):
        # console logger
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # TODO route gevent logs to file
