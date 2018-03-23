import datetime
import logging
import sys
from falcon import Request


logging.StreamHandler(sys.stdout)

logger = logging.getLogger()
logger.addHandler(logging.FileHandler('blog.log'))
logger.setLevel(logging.DEBUG)

def construct_log_message(req: Request, level: str, msg: str):
    """
    Constructs log messages using provided request object.

    :param req: Falcon request object to read from.
    :type req: Request
    :param level: Logging type to tag in logs.
    :type level: str
    :param msg: Message to include in log.
    :type msg: str
    """
    time = datetime.datetime.utcnow()
    message = (f'({level}) time: ["{time}"]; sender: ["{req.forwarded_host}"]; resource: ["{req.path}"];'
               f' method: ["{req.method}"]; message: ["{msg}"];')

    user = req.context.get('user')
    if user:
        return f'user: ["{user.id}", "{user.username}"]; ' + message
    return message


def debug(req: Request, msg: str):
    """
    Create debug message for blog logger.

    :param req: Falcon request object to read from.
    :type req: Request
    :param msg: Message to include in log.
    :type msg: str
    """
    logger.debug(construct_log_message(req, 'debug', msg))


def info(req: Request, msg: str):
    """
    Create info message for blog logger.

    :param req: Falcon request object to read from.
    :type req: Request
    :param msg: Message to include in log.
    :type msg: str
    """
    logger.debug(construct_log_message(req, 'info', msg))


def warning(req: Request, msg: str):
    """
    Create warning message for blog logger.

    :param req: Falcon request object to read from.
    :type req: Request
    :param msg: Message to include in log.
    :type msg: str
    """
    logger.debug(construct_log_message(req, 'warning', msg))


def critical(req: Request, msg: str):
    """
    Create critical message for blog logger.

    :param req: Falcon request object to read from.
    :type req: Request
    :param msg: Message to include in log.
    :type msg: str
    """
    logger.debug(construct_log_message(req, 'critical', msg))
