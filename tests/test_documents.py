#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_documents.py - 

functions:

get_document
get_document_attributes
get_document_content
get_document_file
get_document_files
get_document_links
get_document_preview
get_document_version
get_document_versions
upload_document_file
move_document
delete_document
remove_document_categories
remove_document_category

"""

__author__ = "John van Zantvoort"

import seeddms

from tests.common import SeedDMSWrapper
from tests.vars import *

## class TestGetLockedDocuments(SeedDMSWrapper):
## 
##     def test_get_locked_documents(self):
##         retv = self.sdms.get_locked_documents()
##         self.assertTrue(isinstance(retv, list), "get_locked_documents returns a list item")

if __name__ == '__main__':
    unittest.main()
