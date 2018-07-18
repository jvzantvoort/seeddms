#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""login.py - $description
"""

import argparse
import sys
import os

__author__ = "John van Zantvoort"
__copyright__ = "$copyright"
__email__ = "$mailaddress"
__license__ = "$company"
__version__ = "1.0.1"

import unittest

import seeddms
from seeddms.exceptions import SeedDMSException

CONST_BASEURL = 'http://localhost:8082/restapi/index.php'
CONST_USERNAME = 'admin'
CONST_PASSWORD = 'admin'
CONST_TARGETFOLDER = 'DMS'


class SeedDMSWrapper(unittest.TestCase):
    def setUp(self):
        self.sdms = seeddms.SeedDMS(baseurl = CONST_BASEURL,
                                    username = CONST_USERNAME,
                                    password = CONST_PASSWORD,
                                    targetfolder = CONST_TARGETFOLDER)
        self.sdms.do_login()

    def tearDown(self):
        self.sdms.do_logout()


class TestGetLockedDocuments(SeedDMSWrapper):

    def test_get_locked_documents(self):
        retv = self.sdms.get_locked_documents()
        self.assertTrue(isinstance(retv, list), "get_locked_documents returns a list item")


class TestAccountSettings(SeedDMSWrapper):

    def test_get_account(self):
        retv = self.sdms.get_account()
        self.assertTrue(retv.get('login'), CONST_USERNAME)

    def test_set_email(self):
        orgitem = "address@server.com"
        newitem = "goofy@testme.com"
        self.sdms.set_email(newitem)
        retv = self.sdms.get_account()
        self.sdms.set_email(orgitem)
        self.assertTrue(retv.get('email'), newitem)

    def test_set_full_name(self):
        orgitem = "Administrator"
        newitem = "Goofy"
        self.sdms.set_full_name(newitem)
        retv = self.sdms.get_account()
        self.sdms.set_full_name(orgitem)
        self.assertTrue(retv.get('name'), newitem)

class TestAttributeDefinitions(SeedDMSWrapper):
    def test_get_attribute_definitions(self):
        retv = self.sdms.get_attribute_definitions()
        self.assertTrue(isinstance(retv, list), "get_attribute_definitions returns a list item")

if __name__ == '__main__':
    unittest.main()
