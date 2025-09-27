import platform
import logging
import logging.config
import colorlog

LOGGING_NAME = "FastAPI"

def setup_logging(name=LOGGING_NAME, verbose=True, debug=False):
    level = logging.DEBUG if debug else (logging.INFO if verbose else logging.WARNING)
    # - %(name)s
    formatter_str = "%(asctime)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    # Formatters
    formatters = {
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s" + formatter_str,
            "datefmt": datefmt,
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            }
        }
    }

    # Only console handler
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": level,
            "formatter": "color"
        }
    }

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters,
        "handlers": handlers,
        "loggers": {
            name: {
                "handlers": ["console"],
                "level": level,
                "propagate": False
            }
        }
    })

    # Emoji safe logging cho Windows (nếu cần)
    logger = logging.getLogger(name)
    if platform.system() == 'Windows':
        for fn in logger.info, logger.warning:
            setattr(logger, fn.__name__, lambda x: fn(str(x)))

# Gọi khởi tạo logger
setup_logging(debug=True)
LOGGER = logging.getLogger(LOGGING_NAME)
