#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 test_readEnteredText.py

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
import contextlib
from io import StringIO
""" Third party library """
""" Local library """
from getdoi.reader.readEnteredText import ReadEnteredTextImpl

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class redirect_stdin(contextlib._RedirectStream):
    _stream = "stdin"


class TestReadEnteredTextImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('class TestReadEnteredTextImpl(unittest.TestCase):')
        print('def setUpClass(cls):')

    @classmethod
    def tearDownClass(cls):
        print('def tearDownClass(cls):')

    def setUp(self):
        print('def setUp(self):')
        self.reader = ReadEnteredTextImpl()

    def tearDown(self):
        print('def tearDown(self):')

    def test_hello(self):
        print('def test_hello(self):')
        text = 'Hello, world!'
        buf = StringIO()
        buf.write(text)
        buf.seek(0)
        with redirect_stdin(buf):
            read_text = self.reader.read()
            print(text)
        self.assertEqual(read_text, text)

    def test_exit_commands(self):
        print('def test_exit_commands(self):')
        for exit_text in self.reader.EXIT_TEXTS:
            text = exit_text
            buf = StringIO()
            buf.write(text)
            buf.seek(0)
            with redirect_stdin(buf):
                read_text = self.reader.read()
                print(text)
            self.assertIsNone(read_text)

# ======================================================================================================================


if __name__ == '__main__':
    unittest.main()
