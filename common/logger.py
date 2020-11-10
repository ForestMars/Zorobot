# lib/logger.py - Logging class and functions for Codato.
__version__ = '0.1'
__all__ = ['Log', 'LOG_LEVEL', 'LOG_DIR', 'LOGFILE_NAME']
#import inspect
import logging
import traceback


# Sensible defaults.
LOG_LEVEL = 'DEBUG'
LOG_DIR = 'logs/'
LOGFILE_NAME = 'debug.log'


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(LOG_DIR + LOGFILE_NAME)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.info('Logger initialised by '+' '.join(traceback.format_stack()[0].split()[1:4]))


class Log(object):

    def __init__(self):
        logger.info('Log class initalised by '+' '.join(traceback.format_stack()[0].split()[1:4]))

    @staticmethod
    def info(msg):
        logger.info(msg)

    @staticmethod
    def warn(msg):
        logger.warn(msg)

    @staticmethod
    def debug(msg):
        logger.debug(msg)


def is_debug():
    return logging.getLogger("logger").getEffectiveLevel() == logging.DEBUG


def log(logmsg, lvl='INFO', e=None):
    if e:
        err = ' ('+str(e)+')'+' ERROR: ' + repr(e)
    else:
        err = ''
    logging.lvl(' ' + logmsg + err)


"""
except Exception as e:
    log("Error finding or loading DevelopmentConfig object. You probably need to specify package since Python 3 dropped support for relative import. (See PEP 8)", e)
    try:
        app.config.from_pyfile('config.py')
        log("Loaded configuration from file")
    except IOError:
        log("Error finding config.py", IOError)
    except EOFError:
        log("Error reading config.py (lint file)", EOFError)
    except Exception as e:
        log("Ignoring unknown exception when loading config.py", e)
    except:
        handle_unhandled_error()
        log("no idea.")
"""
