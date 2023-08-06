#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 sciencedirect.py

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

class ScienceDirect(GettableDOI):
    # -- constants --
    # -- constants --
    JOURNAL_URL = 'www.sciencedirect.com'
    JOURNAL_STR = 'ScienceDirect'
    DOI_URL = "https://doi.org/"
    DOI_STR = 'doi: '

    # -- controller --
    def get(self, *, url)->str or None:
        return self.get_url(url=url)

    def get_url(self, *, url)->str or None:
        """return a full URL link"""
        """doiをScienceDirectから読み込む。doiはa hrefのリンクtextである。"""
        # e.g. http://www.sciencedirect.com/science/article/pii/104084289390007Q
        soup = BeautifulSoupModelImpl()
        anchor_links = soup.get_anchor_links(url=url)
        # print(anchor_links)
        """取得した全aタグリンクのうち，指定したジャーナルサイトURLに合致するものを検索"""
        results = []
        for link in anchor_links:
            if self.DOI_URL in link:
                results.append(link)
        # print(results)
        if len(results) > 0:
            # print(results[0])
            return results[0]
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
    def __translate_prev_format(self, *, doi_url):
        """https://doi.org/10.1016/1040-8428(93)90007-Q からdoi_keyを引く。"""
        return self.DOI_STR+doi_url.replace(self.DOI_URL, '')
