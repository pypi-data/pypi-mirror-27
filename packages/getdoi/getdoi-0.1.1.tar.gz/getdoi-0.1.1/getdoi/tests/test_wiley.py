#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 test_wiley.py

Copyright © 2017 Yuto Mizutani.
This software is released under the MIT License.

Version: 1.0.0

TranslateAuthors: Yuto Mizutani
E-mail: yuto.mizutani.dev@gmail.com
Website: http://operantroom.com

Created: 2017/12/09
Device: MacBook Pro (Retina, 13-inch, Mid 2015)
OS: macOS Serria version 10.12.6
IDE: PyCharm Community Edition 2017.2.4
Python: 3.6.1
"""

# --- References ---
# --- notes ---
# --- Information ---
# --- Circumstances ---

# === import ===========================================================================================================

""" Standard library """
import unittest
""" Third party library """
""" Local library """
from getdoi.getDOIFromURL.wiley import Wiley

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class TestWiley(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('class TestWiley(unittest.TestCase):')
        print('def setUpClass(cls):')

    @classmethod
    def tearDownClass(cls):
        print('def tearDownClass(cls):')

    def setUp(self):
        print('def setUp(self):')
        self.getter = Wiley()

    def tearDown(self):
        print('def tearDown(self):')

    def test_get_url(self):
        print('def test_get_url(self):')
        url = 'http://onlinelibrary.wiley.com/doi/10.1901/jeab.1963.6-s477/full'
        doi_url = 'https://doi.org/10.1901/jeab.1963.6-s477'
        result = self.getter.get_url(url=url)
        print('URL: {0}'.format(url))
        print('DOI: {0}'.format(result))
        self.assertEqual(result, doi_url)

    def test_get_prev_format(self):
        print('def test_get_prev_format(self):')
        url = 'http://onlinelibrary.wiley.com/doi/10.1901/jeab.1963.6-s477/full'
        prev_doi = 'doi: 10.1901/jeab.1963.6-s477'
        result = self.getter.get_prev_format(url=url)
        print('URL: {0}'.format(url))
        print('DOI: {0}'.format(result))
        self.assertEqual(result, prev_doi)

# ======================================================================================================================


if __name__ == '__main__':
    unittest.main()
