#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Standard lib imports
import time
import random
# Third Party imports
import threading
# BITSON imports
from logger import logger
from controller import Controller


if __name__ == '__main__':
    controller = Controller()
    controller.run()