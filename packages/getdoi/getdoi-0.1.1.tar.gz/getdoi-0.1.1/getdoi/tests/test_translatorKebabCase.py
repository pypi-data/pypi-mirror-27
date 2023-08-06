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
from getdoi.translator.translatorKebabCase import *

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class TestTranslatorKebabCaseImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('class TestTranslatorKebabCaseImpl(unittest.TestCase):')
        print('def setUpClass(cls):')

    @classmethod
    def tearDownClass(cls):
        print('def tearDownClass(cls):')

    def setUp(self):
        print('def setUp(self):')
        self.translator = TranslatorKebabCaseImpl()

    def tearDown(self):
        print('def tearDown(self):')

    def test_Ordinary_sentences(self):
        print('def test_Ordinary_sentences(self):')
        text = 'ABA Single-subject experimental design'
        correct = 'aba-single-subject-experimental-design'
        self.assertEqual(self.translator.translate(text), correct)

    def test_CamelCaseIncludeUpperProperNoun(self):
        print('def test_CamelCaseIncludeUpperProperNoun(self):')
        text = 'ABASingleSubjectExperimentalDesign'
        correct = 'aba-single-subject-experimental-design'
        self.assertEqual(self.translator.translate(text), correct)

    def test_snake_case_include_upper_proper_noun(self):
        print('def test_snake_case_include_upper_proper_noun(self):')
        text = 'ABA_single_subject_experimental_design'
        correct = 'aba-single-subject-experimental-design'
        self.assertEqual(self.translator.translate(text), correct)

# ======================================================================================================================


if __name__ == '__main__':
    unittest.main()
