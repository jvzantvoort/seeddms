#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_attributedefinitions.py - 

functions:

- get_attribute_definitions
- change_attribute_definition_name

"""

__author__ = "John van Zantvoort"

import unittest

import seeddms
from tests.common import SeedDMSWrapper
from tests.vars import *

class TestAttributeDefinitions(SeedDMSWrapper):

    def test_get_attribute_definitions(self):
        retv = self.sdms.get_attribute_definitions()
        self.assertTrue(isinstance(retv, list), "get_attribute_definitions returns a list item")

    @unittest.skip("unknown ways to create attribute_definitions")
    def test_change_attribute_definition_name(self):
        """

        """
        pass

if __name__ == '__main__':
    unittest.main()
