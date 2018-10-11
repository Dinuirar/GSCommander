#!/usr/bin/env python
import logging
import datetime
# later may be used to hold all logging functionality


def log_init():
    """Configure logging"""
    log_name = datetime.datetime.now().strftime("%y%m%d") + ".log"
    log_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s",
                                      datefmt='%Y/%m/%d %H:%M:%S'
                                      )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # TODO: later set level to logging.INFO

    # handler for logging to file
    file_handler = logging.FileHandler(log_name)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)


def log_exception(msg):
    """For convenience. Logs and prints on screen"""
    logging.exception(msg=msg)
    #print(msg)


def log_error(msg):
    """For convenience. Logs and prints on screen"""
    logging.error(msg=msg)
    print(msg)


def log_warning(msg):
    """For convenience. Logs and prints on screen"""
    logging.warning(msg=msg)
    print(msg)


def log_info(msg):
    """For convenience. Logs and prints on screen"""
    logging.info(msg=msg)
    print(msg)

# handler for logging into stream
# console_handler = logging.StreamHandler()
# #console_handler = logging.StreamHandler(sys.stdout)
# root_logger.addHandler(console_handler)
