#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 test_translatorScholarQuery.py

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
from getdoi.getArticleURL.translateGoogleScholarQuery import TranslateGoogleScholarQuery

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class TestTranslatorScholarQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('class TestTranslatorScholarQuery(unittest.TestCase):')
        print('def setUpClass(cls):')

    @classmethod
    def tearDownClass(cls):
        print('def tearDownClass(cls):')

    def setUp(self):
        print('def setUp(self):')
        self.translator = TranslateGoogleScholarQuery()

    def tearDown(self):
        print('def tearDown(self):')

    def testQueryScholarOne(self):
        print('def testQueryScholarOne(self):')
        citation = 'Howe, K., Clark, M. D., Torroja, C. F., Torrance, J., Berthelot, C., Muffato, M., ... & McLaren, S. (2013). The zebrafish reference genome sequence and its relationship to the human genome. Nature, 496(7446), 498-503.'
        print(citation)
        first_author = 'Howe, K.'
        title = 'The zebrafish reference genome sequence and its relationship to the human genome.'
        url = self.translator.translate(first_author, title)
        self.assertEqual(url, 'https://scholar.google.com/scholar?q=author%3A%22howe+k%22+intitle%3A%22The+zebrafish+reference+genome+sequence+and+its+relationship+to+the+human+genome.%22')

    def testQueryScholarTwo(self):
        print('def testQueryScholarTwo(self):')
        # author:"fleshler m" intitle:"A progression for generating variable-interval schedules."
        # https://scholar.google.com/scholar?q=author%3A%22fleshler+m%22+intitle%3A%22A+progression+for+generating+variable-interval+schedules.%22
        citation = 'Fleshler, M., & Hoffman, H. S. (1962). A progression for generating variable-interval schedules. Journal of the experimental analysis of behavior, 5(4), 529.'
        print(citation)
        first_author = 'Fleshler, M.'
        title = 'A progression for generating variable-interval schedules.'
        url = self.translator.translate(first_author, title)
        self.assertEqual(url, 'https://scholar.google.com/scholar?q=author%3A%22fleshler+m%22+intitle%3A%22A+progression+for+generating+variable-interval+schedules.%22')


# ======================================================================================================================


if __name__ == '__main__':
    unittest.main()
