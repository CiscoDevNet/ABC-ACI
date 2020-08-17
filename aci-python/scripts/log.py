import logging
import logging.handlers as handlers
import os
import argparse
import json


class CustomFormatter(logging.Formatter):
    def __init__(self, patterns=[], fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.patterns = patterns

    def format(self, record: logging.LogRecord):
        res = super(CustomFormatter, self).format(record)
        for pattern in self.patterns:
            res = res.replace(pattern, "*******")
        return res

def default(name, level="INFO", patterns=[], logfile=None):
    ch = logging.StreamHandler()
    custom_formatter = CustomFormatter(patterns=patterns, fmt="[%(asctime)s] [%(levelname)8s] (%(filename)s:%(lineno)s) --- %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    ch.setLevel(level)
    logger = logging.getLogger(name)
    logger.handlers = []

    ch.setFormatter(custom_formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    if not logfile == None:
        # 100 MB Log Files
        rfh = handlers.RotatingFileHandler(logfile, mode='a+',maxBytes=104857600, backupCount=2)
        rfh.setLevel(logging.DEBUG)
        rfh.setFormatter(custom_formatter)
        logger.addHandler(rfh)
    return logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Logging Examples')
    parser.add_argument('--log', default="INFO")
    parser.add_argument('--logfile', default="aci.log")
    args = parser.parse_args()
    logger = default("aci-basics", level=args.log, logfile=args.logfile)
    logger.debug(os.environ)
    logger.info("creating aci tenant")
    logger.warning("using default password: Cisco12345")

    logger.fatal("program has encountered a critical error")
    logger = default("aci-basics", patterns=["Cisco12345"], level=args.log, logfile=args.logfile)
    logger.info("using default password: Cisco12345")

