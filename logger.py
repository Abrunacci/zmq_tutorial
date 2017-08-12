# -*- coding: utf-8 -*-
# Standard lib imports
import logging.handlers
import time
# Third Party imports

# BITSON imports

__version__ = '0.1.0'
__all__ = ["server"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_format = "".join(["[%(asctime)s] %(name)20s - %(levelname)8s: ",
                      "%(threadName)15s - %(funcName)15s() - %(message)s"])

formatter = logging.Formatter(fmt=log_format)
# Format UTC Time
formatter.converter = time.gmtime

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)
