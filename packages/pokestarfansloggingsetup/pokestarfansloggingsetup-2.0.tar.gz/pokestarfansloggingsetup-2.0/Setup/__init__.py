from datetime import datetime
import logging
import os
import sys

def setup_logger(name, loglevel=logging.INFO):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = logging.FileHandler(filename='logs/{}_{}.log'.format(name, datetime.now().strftime('%m_%d_%y')))
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=loglevel,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} (%(funcName)s) %(levelname)s - %(message)s',
        handlers=handlers
    )

    logger = logging.getLogger(__name__)
    return logger
