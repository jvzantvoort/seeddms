#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_account.py - 

functions:

- get_account
- get_locked_documents
- set_email
- set_full_name

"""

__author__ = "John van Zantvoort"

import seeddms

from tests.common import SeedDMSWrapper
from tests.vars import *

class TestGetLockedDocuments(SeedDMSWrapper):

    def test_get_locked_documents(self):
        retv = self.sdms.get_locked_documents()
        self.assertTrue(isinstance(retv, list), "get_locked_documents returns a list item")


class TestGetLockedDocuments(SeedDMSWrapper):

    def test_get_locked_documents(self):
        retv = self.sdms.get_locked_documents()
        self.assertTrue(isinstance(retv, list), "get_locked_documents returns a list item")

class TestAccountSettings(SeedDMSWrapper):

    def test_get_account(self):
        retv = self.sdms.get_account()
        self.assertTrue(retv.get('login'), CONST_USERNAME)

    @unittest.skip("functionality does not seem to be implemented.")
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

if __name__ == '__main__':
    unittest.main()
