#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 test_psycnet.py

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
from getdoi.getDOIFromURL.psycnet import PsycNET
from getdoi.getDOIFromURL.psycnet import SSLStateInPsycNET

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class TestPsycNET(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('class TestPsycNET(unittest.TestCase):')
        print('def setUpClass(cls):')

    @classmethod
    def tearDownClass(cls):
        print('def tearDownClass(cls):')

    def setUp(self):
        print('def setUp(self):')
        self.getter = PsycNET()

    def tearDown(self):
        print('def tearDown(self):')

    def test_SSLStateInPsycNET(self):
        print('def test_SSLStateInPsycNET(self):')
        ssl_on = SSLStateInPsycNET()
        self.assertEqual(ssl_on.get_doi_url('https://'), 'https://dx.doi.org/')
        self.assertEqual(ssl_on.get_psycnet_url('https://'), 'https://psycnet.apa.org/doi/')
        ssl_off = SSLStateInPsycNET()
        self.assertEqual(ssl_off.get_doi_url('http://'), 'http://dx.doi.org/')
        self.assertEqual(ssl_off.get_psycnet_url('http://'), 'http://psycnet.apa.org/doi/')

    def test_get_url(self):
        print('def test_get_url(self):')
        url = 'http://psycnet.apa.org/journals/amp/18/8/503/'
        doi = 'http://dx.doi.org/10.1037/h0045185'
        result = self.getter.get_url(url=url)
        print('URL: {0}'.format(url))
        print('DOI: {0}'.format(result))
        self.assertEqual(result, doi)

    def test_get_prev_format(self):
        print('def test_get_prev_format(self):')
        url = 'http://psycnet.apa.org/journals/amp/18/8/503/'
        doi = 'doi: 10.1037/h0045185'
        result = self.getter.get_prev_format(url=url)
        print('URL: {0}'.format(url))
        print('DOI: {0}'.format(result))
        self.assertEqual(result, doi)

# ======================================================================================================================


if __name__ == '__main__':
    unittest.main()
