#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 wiley.py

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


# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================

class Wiley(GettableDOI):
    # -- constants --
    JOURNAL_URL = 'onlinelibrary.wiley.com'
    JOURNAL_STR = 'Wiley'
    DOI_KEY = "doi/"
    DOI_KEY_FULL = "/full"
    DOI_URL = 'https://doi.org/'
    DOI_STR = 'doi: '


    # -- controller --
    def get(self, *, url: str)->str or None:
        return self.get_url(url=url)

    def get_url(self, *, url: str)->str or None:
        raw_doi = self.__get_raw_doi(url=url)
        if raw_doi is None:
            return None
        else:
            return self.__translate_url_format(raw_doi=raw_doi)

    def get_prev_format(self, *, url: str)->str or None:
        raw_doi = self.__get_raw_doi(url=url)
        if raw_doi is None:
            return None
        else:
            return self.__translate_prev_format(doi_url=raw_doi)


    # -- translator --
    def __translate_url_format(self, *, raw_doi: str)->str:
        """10.1901/jeab.1963.6-s477 に https://dx.doi.org/ を加える。"""
        return self.DOI_URL+raw_doi

    def __translate_prev_format(self, *, doi_url: str)->str:
        """10.1901/jeab.1963.6-s477 に doi: を加える。"""
        return self.DOI_STR + doi_url.replace(self.DOI_URL, '')

    # -- model --
    def __get_raw_doi(self, *, url: str)->str or None:
        """doiをwileyから読み込む。が，wileyは元々doiがURLに含まれている。"""
        # e.g. "http://onlinelibrary.wiley.com/doi/10.1901/jeab.1963.6-s477/full"
        if self.__decision_include_keyword(keyword=self.DOI_KEY, text=url):
            wiley_url = url
            if self.__decision_include_keyword(keyword=self.DOI_KEY_FULL, text=url):
                # /fullが含まれていれば予め削除しておく。
                wiley_url = url[0:-(len(self.DOI_KEY_FULL))]
            num = wiley_url.find(self.DOI_KEY)
            count = 0
            doi = ""
            for char in wiley_url:
                if count >= num + len(self.DOI_KEY):
                    doi += char
                count += 1
            # 10.1901/jeab.1963.6-s477
            # print(doi)
            return doi
        else:
            print("含まれない！？ scrapingを用いた検索処理は未実装です。")
            print('NoneDOI From Wiley ({link})'.format(link=url))
            return None

    def __decision_include_keyword(self, *, keyword: str, text: str):
        """[text]から[keywordを検索] -> Bool """
        if keyword == '':
            return False
        # print(searchWord in text)
        return keyword in text
