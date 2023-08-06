#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 nature.py

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

class Nature(GettableDOI):
    # https://www.nature.com/articles/ng1000_216
    # doi:10.1038/79951
    # -- constants --
    JOURNAL_URL = 'www.nature.com'
    JOURNAL_STR = 'nature'
    DOI_KEY = 'doi:'
    DOI_URL = "https://doi.org/"
    DOI_STR = 'doi: '
    META_KEY = 'name'
    META_ID = 'prism.doi'

    # 1. meta contentから探す
    # 2. 平文から探す。

    # -- controller --
    def get(self, *, url)->str or None:
        return self.get_url(url=url)

    def get_url(self, *, url)->str or None:
        """return a full URL link"""
        soup = BeautifulSoupModelImpl()
        """doiを読み込む。doiはmeta内である。"""
        raw_doi = soup.get_meta_content(url=url, key=self.META_KEY, id=self.META_ID)
        # print(raw_doi)
        if raw_doi is not None:
            doi_url = self.__translate_url(raw_doi=raw_doi)
            return doi_url
        # 見つからなかった場合：
        """doiを読み込む。doiは平文text，data-track-sourceである。"""
        data_track_sources = soup.get_data_track_sources(url=url)
        # print(data_track_sources)
        """取得した全data-track-sourceのうち，"doi:"に合致するものを検索。"""
        """doi:(スペースなし)に合致するものは複数あるが，どれも当該articleのdoiなので[0]で返す。"""
        results = []
        for source in data_track_sources:
            if self.DOI_KEY in source:
                results.append(source)
        # print(results)
        if len(results) > 0:
            # print(results[0])
            doi_url = self.__translate_url(raw_doi=results[0])
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
        """doi:10.1038/79951からdoi:を引き，https://dx.doi.org/を加える。"""
        return self.DOI_URL+raw_doi.replace(self.DOI_KEY, '')

    def __translate_prev_format(self, *, doi_url):
        """https://dx.doi.org/10.1038/79951からhttps://dx.doi.org/を引きdoi: を加える。"""
        return self.DOI_STR+doi_url.replace(self.DOI_URL, '')
