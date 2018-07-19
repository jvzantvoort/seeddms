#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_login.py 

functions:

do_login
do_logout

"""

__author__ = "John van Zantvoort"

import unittest

import seeddms

from tests.common import SeedDMSWrapper
from tests.vars import *

class TestLogin(SeedDMSWrapper):


    def test_login(self):
        self.do_login(CONST_USERNAME, CONST_PASSWORD)

if __name__ == '__main__':
    unittest.main()
