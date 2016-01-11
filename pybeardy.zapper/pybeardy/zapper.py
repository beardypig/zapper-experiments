#!/usr/bin/env python
import logging
from collections import namedtuple

import serial

log = logging.getLogger(__name__)


class ZapState(namedtuple("ZapState", ["trigger", "detect"])):
    pass


class ZapSerial(object):
    def __init__(self, port, baud=9600):
        self.serial = serial.Serial(port, baud, timeout=1.0)
        self.state = ZapState(0, 0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def update(self):
        # send one byte to read and reset the state
        self.serial.write(bytes('\x01'))
        rstate = ord(self.serial.read() or '\x00')
        self.state = ZapState(bool(rstate & 0x2), bool(rstate & 0x1))
        return self.state

    def close(self):
        self.serial.close()
