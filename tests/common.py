#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""common.py - 

"""

__author__ = "John van Zantvoort"

try:
    import unittest2 as unittest  # NOQA
except ImportError:  # Python >= 2.7
    import unittest  # NOQA

import seeddms

from tests.vars import *

class SeedDMSWrapper(unittest.TestCase):
    def setUp(self):
        self.sdms = seeddms.SeedDMS(baseurl = CONST_BASEURL,
                                    username = CONST_USERNAME,
                                    password = CONST_PASSWORD,
                                    targetfolder = CONST_TARGETFOLDER)
        self.sdms.do_login()

    def tearDown(self):
        self.sdms.do_logout()

    def do_login(self, username, password):
        test_sdms = seeddms.SeedDMS(baseurl = CONST_BASEURL,
                                    username = username,
                                    password = password,
                                    targetfolder = CONST_TARGETFOLDER)
        test_sdms.do_login()
        test_sdms.do_logout()

class SeedDMSCategoryWrapper(unittest.TestCase):
    def setUp(self):
        self.sdms = seeddms.SeedDMS(baseurl = CONST_BASEURL,
                                    username = CONST_USERNAME,
                                    password = CONST_PASSWORD,
                                    targetfolder = CONST_TARGETFOLDER)
        self.sdms.do_login()

        if not self.sdms.has_category(CONST_CAT01):
            self.sdms.create_category(CONST_CAT01)

    def tearDown(self):
        for row in self.sdms.get_categories():
            idn = row['id']
            self.sdms.delete_category(idn)

        self.sdms.do_logout()

    def do_login(self, username, password):
        test_sdms = seeddms.SeedDMS(baseurl = CONST_BASEURL,
                                    username = username,
                                    password = password,
                                    targetfolder = CONST_TARGETFOLDER)
        test_sdms.do_login()
        test_sdms.do_logout()

