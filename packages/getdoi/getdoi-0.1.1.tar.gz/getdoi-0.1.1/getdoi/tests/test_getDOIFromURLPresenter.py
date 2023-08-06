#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 test_getDOIFromURLPresenterImpl.py

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
[io]
https://qiita.com/podhmo/items/70a78c1429525dde0a48
"""
# --- notes ---
# --- Information ---
# --- Circumstances ---

# === import ===========================================================================================================

""" Standard library """
import unittest
""" Third party library """
""" Local library """
from getdoi.getDOIFromURL.getDOIFromURLController import GetDOIFromURLControllerImpl

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================
html_yahoo = None

# ======================================================================================================================


class TestGetDOIFromURLPresenterImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('class GetDOIFromURLPresenterImpl(unittest.TestCase):')
        print('def setUpClass(cls):')

    @classmethod
    def tearDownClass(cls):
        print('def tearDownClass(cls):')

    def setUp(self):
        print('def setUp(self):')
        self.presenter = GetDOIFromURLControllerImpl()

    def tearDown(self):
        print('def tearDown(self):')



    def test_html(self):
        print('def test_html(self):')
        url = 'https://www.yahoo.co.jp/'
        html = self.soup.get_html(url)
        self.assertIsNotNone(html)

    def test_get_anchors(self):
        print('def test_get_anchors(self):')
        url = 'https://www.yahoo.co.jp/'
        anchors = self.soup.get_anchors(url)
        self.assertIsNotNone(anchors)

    def test_get_anchor_links(self):
        print('def get_anchor_links(self):')
        url = 'https://www.yahoo.co.jp/'
        anchors = self.soup.get_anchor_links(url)
        self.assertIsNotNone(anchors)

    def test_get_anchor_texts(self):
        print('def get_anchor_texts(self):')
        url = 'https://www.yahoo.co.jp/'
        anchors = self.soup.get_anchor_texts(url)
        self.assertIsNotNone(anchors)

# ======================================================================================================================


if __name__ == '__main__':
    unittest.main()
