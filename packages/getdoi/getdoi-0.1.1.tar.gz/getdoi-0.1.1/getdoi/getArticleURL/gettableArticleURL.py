#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 gettableArticleURL.py

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
""" Third party library """
from articleinfo.articleInfo import ArticleInfo
""" Local library """

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class GettableArticleURL(object):
    # -- constants --
    SCHOLAR_URL = None

    # -- funcs --
    def get(self, *, article_info: ArticleInfo)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError
