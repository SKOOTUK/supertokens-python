import logging
import logging.config


LOGGER_NAME = "falcon-middleware"
LOGGER_CONF = {
    "version": 1,
    "formatters": {
        "basic": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "handler1": {
            "class": "logging.StreamHandler",
            "formatter": "basic",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        LOGGER_NAME: {
            "handlers": ["handler1"],
            "level": "INFO",
        },
    },
}


def set_logger():
    logging.config.dictConfig(LOGGER_CONF)
    return get_logger()


def get_logger():
    return logging.getLogger(LOGGER_NAME)
