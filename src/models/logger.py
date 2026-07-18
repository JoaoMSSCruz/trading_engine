import logging

class Logger:
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger("Trading Engine")