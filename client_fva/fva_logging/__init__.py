import logging

from client_fva.user_settings import UserSettings
from .core import Handler
from .gui import LoggingDialog

logging_window = None

def get_loggin_window():
    global logging_window
    if logging_window is None:
        logging_window = LoggingDialog()
    return logging_window

def configure_settings(settings=UserSettings.getInstance()):
    logging_window = get_loggin_window()
    logger = logging.getLogger()
    ch = logging_window.handler
    formatter = logging.Formatter(settings.logging_formater)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(settings.logging_level)