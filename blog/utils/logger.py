import logging


def construct_log_message(req, msg):
    """
    """
    message = (f'sender: ["{req.forwarded_host}"]; resource: ["{req.path}"];'
               f' method: ["{req.method}"]')
    if req.blog_user:
        return f'user: ["{req.blog_user.user_id}", "{req.blog_user.username}"]; ' + message
    return message


def debug(req, msg):
    """
    """
    logging.debug(construct_log_message(req, msg))

def info(req, msg):
    """
    """
    logging.debug(construct_log_message(req, msg))

def warning(req, msg):
    """
    """
    logging.debug(construct_log_message(req, msg))
