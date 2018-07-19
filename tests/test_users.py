#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_users.py - 

functions:

- get_users
- get_user_by_name
- get_user_by_id
- create_user
set_disabled_user
set_enabled_user
- encpasswd
change_user_password
- delete_user

"""

__author__ = "John van Zantvoort"

import seeddms

from tests.common import SeedDMSWrapper
from tests.vars import *

class TestPassword(SeedDMSWrapper):

    def test_encpasswd(self):
        md5str1 = 'e2798af12a7a0f4f70b4d69efbc25f4d'
        md5str2 = self.sdms.encpasswd('redhat')
        self.assertEqual(md5str1, md5str2)

class TestCreateUser(SeedDMSWrapper):

    def user_exists(self, username):
        test_data = None
        try:
            test_data = self.sdms.get_user_by_name(username)

        except SeedDMSException:
            return False

        if test_data is None:
            return False

        if not isinstance(test_data, dict):
            self.fail("not a dict " + str(test_data))

        if test_data.get('login') == username:
            return True
        else:
            return False

    def test_create_delete_user(self):
        """test for user creation/deletion

        """
        tst01_login = CONST_TEST1_DATA.get('login')
        tst01_name = CONST_TEST1_DATA.get('name')
        tst01_email = CONST_TEST1_DATA.get('email')

        user_exists = self.user_exists(tst01_login)

        if user_exists:
            idn = self.sdms.get_user_by_name(tst01_login)
            self.sdms.delete_user(idn['id'])

        retv = self.sdms.create_user(user=tst01_login,
                                     password=CONST_TEST1_PASS,
                                     name=tst01_name,
                                     email=tst01_email)

        user_exists = self.user_exists(tst01_login)

        self.do_login(tst01_login, CONST_TEST1_PASS)

        if user_exists:
            idn = self.sdms.get_user_by_name(tst01_login)
            self.sdms.delete_user(idn['id'])


        self.assertTrue(user_exists)

class TestUsers(SeedDMSWrapper):


    def test_get_users(self):
        ref_data = {u'admin': u'admin', u'guest': u'guest'}
        test_data = dict()
        for row in self.sdms.get_users():
            row_role = row.get('role')
            row_login  = row.get('login')
            test_data[row_login] = row_role

        compare_dictionary(ref_data, test_data)

    def test_get_user_by_name(self):

        test_data = self.sdms.get_user_by_name('admin')
        if not isinstance(test_data, dict):
            self.fail("not a dict")

        compare_dictionary(CONST_ADMIN_DATA, test_data)

    def test_get_user_by_id(self):

        test_data = self.sdms.get_user_by_id(CONST_ADMIN_DATA['id'])
        if not isinstance(test_data, dict):
            self.fail("not a dict")

        compare_dictionary(CONST_ADMIN_DATA, test_data)

class TestGetLockedDocuments(SeedDMSWrapper):

    def test_get_locked_documents(self):
        retv = self.sdms.get_locked_documents()
        self.assertTrue(isinstance(retv, list), "get_locked_documents returns a list item")

if __name__ == '__main__':
    unittest.main()
