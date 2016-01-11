#!/usr/bin/env python
import unittest

from pybeardy.zapper import ZapState


class ZapStateTest(unittest.TestCase):
    def test_state(self):
        s = ZapState(True, True)
        self.assertTrue(s.detect)
        self.assertTrue(s.trigger)


if __name__ == '__main__':
    unittest.main()
