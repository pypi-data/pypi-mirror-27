#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 test_translatorKebabCase.py

Copyright © 2017 Yuto Mizutani.
This software is released under the MIT License.

Version: 1.0.0

TranslateAuthors: Yuto Mizutani
E-mail: yuto.mizutani.dev@gmail.com
Website: http://operantroom.com

Created: 2017/12/07
Device: MacBook Pro (Retina, 13-inch, Mid 2015)
OS: macOS Serria version 10.12.6
IDE: PyCharm Community Edition 2017.2.4
Python: 3.6.1
"""

# --- References ---
"""
[Test]
http://futurismo.biz/archives/4395
"""
# --- notes ---
"""
初めて作成したユニットテスト。
"""
# --- Information ---
# --- Circumstances ---

# === import ===========================================================================================================

""" Standard library """
import unittest
""" Third party library """
""" Local library """
from articleinfo.tests.test_apa import TestAPA

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================


# ======================================================================================================================

class TestAll(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('class TestAll(unittest.TestCase):')
        print('def setUpClass(cls):')
        cls.testAPA = TestAPA()
        pass

    @classmethod
    def tearDownClass(cls):
        print('def tearDownClass(cls):')
        pass

    def setUp(self):
        print('def setUp(self):')

    def tearDown(self):
        print('def tearDown(self):')
        pass

# ======================================================================================================================


if __name__ == '__main__':
    unittest.main()
