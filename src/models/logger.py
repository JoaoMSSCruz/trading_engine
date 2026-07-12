import logging

class Logger:
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger("Trading Engine")