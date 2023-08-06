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
from getdoi.tests.test_readEnteredText import TestReadEnteredTextImpl
from getdoi.tests.test_translatorKebabCase import TestTranslatorKebabCaseImpl
from getdoi.tests.test_beautifulSoupModel import TestReadEnteredTextImpl
from getdoi.tests.test_sciencedirect import TestScienceDirect
from getdoi.tests.test_wiley import TestWiley
from getdoi.tests.test_springer import TestSpringer
from getdoi.tests.test_psycnet import TestPsycNET
from getdoi.tests.test_plos import TestPLOS
from getdoi.tests.test_pmc import TestPMC

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================


# ======================================================================================================================

class TestAll(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('class TestTranslatorKebabCaseImpl(unittest.TestCase):')
        print('def setUpClass(cls):')
        cls.testReadEnteredTextImpl = TestReadEnteredTextImpl()
        cls.testTranslatorKebabCaseImpl = TestTranslatorKebabCaseImpl()
        cls.testReadEnteredTextImpl = TestReadEnteredTextImpl()
        cls.testScienceDirect = TestScienceDirect()
        cls.testWiley = TestWiley()
        cls.testSpringer = TestSpringer()
        cls.testPsycNET = TestPsycNET()
        cls.testPLOS = TestPLOS()
        cls.testPMC = TestPMC()
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
