#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 gettableDOI.py

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
""" Local library """

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class GettableDOI(object):
    # -- constants --
    JOURNAL_URL = None
    JOURNAL_STR = None

    def get(self, *, url: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_url(self, *, url: str)->str or None:
        """return a full URL link"""
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_prev_format(self, *, url: str)->str or None:
        """doi：[space] [doinumber]"""
        print('Error! Can not call protocol funcs!')
        raise RuntimeError
