import logging
import os
import coloredlogs

from vHunter.utils import Config
from vHunter.utils.distro import get_distro

levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
}


def setup_logging(log_file=None, log_level=None):
    config = Config()
    if log_file is None:
        log_file = config.log_file[get_distro()]
    if log_level is None:
        log_level = config.log_level
    log_level = log_level.upper()

    os.environ['COLOREDLOGS_LOG_FORMAT'] = config.log_format

    make_dirs(log_file)
    logger = logging.getLogger()
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter(config.log_format))
    logger.addHandler(handler)
    logger.setLevel(log_level)
    coloredlogs.install(
        level=levels[log_level]
    )
    return [handler.stream.fileno()]


def make_dirs(log_file):
    dir_name = os.path.dirname(log_file)
    os.makedirs(dir_name, exist_ok=True)
