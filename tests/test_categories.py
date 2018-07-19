#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_categories.py - 

functions:

- get_categories
- lookup_category_id
- get_category
- create_category
- change_category_name
- delete_category

"""

__author__ = "John van Zantvoort"

import unittest
import random, string
import seeddms

from tests.common import SeedDMSWrapper, SeedDMSCategoryWrapper, unittest
from tests.vars import *

class TestCreateDeleteCategory(SeedDMSCategoryWrapper):

    def test_create_category(self):
        cat_chars = string.ascii_uppercase + string.digits
        category_name = ''.join(random.choice(cat_chars) for _ in range(16))

        if self.sdms.has_category(category_name):
            cat_id = self.sdms.lookup_category_id(category_name)
            self.sdms.delete_category(cat_id)

        self.sdms.create_category(category_name)
        self.assertTrue(self.sdms.has_category(category_name))

class TestGetCategories(SeedDMSCategoryWrapper):

    def test_get_categories(self):

        cat_chars = string.ascii_uppercase + string.digits
        category_names1 = list()
        category_names2 = list()

        for x in range(0, 10):
            category_names1.append(''.join(random.choice(cat_chars) for _ in range(16)))

        for category_name in category_names1:
            self.sdms.create_category(category_name)

        for row in self.sdms.get_categories():
            if row['name'] in category_names1:
                category_names2.append(row['name'])
        self.assertEqual(len(category_names1), len(category_names2))

class TestChangeCategoryName(SeedDMSCategoryWrapper):

    def test_move_category(self):
        cat_chars = string.ascii_uppercase + string.digits
        category_name1 = ''.join(random.choice(cat_chars) for _ in range(16))
        category_name2 = ''.join(random.choice(cat_chars) for _ in range(16))

        if not self.sdms.has_category(category_name1):
            self.sdms.create_category(category_name1)

        cat_id1 = self.sdms.lookup_category_id(category_name1)
        self.sdms.change_category_name(cat_id1, category_name2)
        cat_id2 = self.sdms.lookup_category_id(category_name2)

        self.assertEqual(cat_id1, cat_id2)

if __name__ == '__main__':
    unittest.main()
