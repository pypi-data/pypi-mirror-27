#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 science.py

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
from .gettableDOI import GettableDOI
from getdoi.scraping.beautifulSoupModel import BeautifulSoupModelImpl

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================

class Science(GettableDOI):
    # http://science.sciencemag.org/content/309/5732/3106
    # 10.1126/science.1114519
    # -- constants --
    JOURNAL_URL = 'science.sciencemag.org'
    JOURNAL_STR = 'Science'
    DOI_KEY = 'DOI: '
    DOI_URL = "https://doi.org/"
    DOI_STR = 'doi: '
    META_KEY = 'name'
    META_ID = 'citation_doi'

    # natureは平文にdoi:10.1038/79951と記載されているのみである。

    # -- controller --
    def get(self, *, url)->str or None:
        return self.get_url(url=url)

    def get_url(self, *, url)->str or None:
        """return a full URL link"""
        """doiを読み込む。doiはmeta内である。"""
        soup = BeautifulSoupModelImpl()
        raw_doi = soup.get_meta_content(url=url, key=self.META_KEY, id=self.META_ID)
        # print(raw_doi)
        if raw_doi is not None:
            doi_url = self.__translate_url(raw_doi=raw_doi)
            return doi_url
        else:
            print('Any DOI found from {journal} ({link})'.format(journal=self.JOURNAL_STR, link=url))
            return None

    def get_prev_format(self, *, url)->str or None:
        """doi：[space] [doinumber]"""
        doi_url = self.get_url(url=url)
        if doi_url is None:
            return None
        else:
            return self.__translate_prev_format(doi_url=doi_url)

    # -- translator --
    def __translate_url(self, *, raw_doi):
        """10.1126/science.1114519からhttps://dx.doi.org/を加える。"""
        return self.DOI_URL+raw_doi

    def __translate_prev_format(self, *, doi_url):
        """https://doi.org/10.1126/science.1114519からhttps://doi.org/を引きdoi: を加える。"""
        return self.DOI_STR+doi_url.replace(self.DOI_URL, '')
