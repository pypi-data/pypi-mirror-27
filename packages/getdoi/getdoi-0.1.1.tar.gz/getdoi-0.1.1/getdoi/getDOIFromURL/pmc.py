#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 pmc.py

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


class PMC(GettableDOI):
    # -- constants --
    JOURNAL_URL = 'www.ncbi.nlm.nih.gov/pmc'
    JOURNAL_STR = 'PMC'
    DOI_URL = 'https://dx.doi.org/'
    DOI_STR = 'doi: '
    DOI_URL_NETWORK_PATH = '//dx.doi.org/'
    NETWORK_PATH = 'https:'

    # -- controller --
    def get(self, *, url: str)->str or None:
        return self.get_url(url=url)

    def get_url(self, *, url: str)->str or None:
        """doiをPMCから読み込む。doiはanchor_textである。が，検索できないため，anchor_linksより行う。"""
        # e.g. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1333534/
        soup = BeautifulSoupModelImpl()
        anchor_links = soup.get_anchor_links(url)
        # print(anchor_links)
        """取得した全aタグリンクのうち，指定したジャーナルサイトURLに合致するものを検索"""
        # __find_https_format()
        doi = self.__find_https_format(anchor_links=anchor_links)
        if doi is not None:
            return self.__translate_decode(doi)

        # __find_network_path_reference_format()
        doi = self.__find_network_path_reference_format(anchor_links=anchor_links)
        if doi is not None:
            return self.__translate_decode(doi)

        print('AnyDOI From PMC ({link})'.format(link=url))
        return None

    def get_prev_format(self, *, url: str)->str or None:
        """doi：[space] [doinumber]"""
        doi_url = self.get_url(url=url)
        if doi_url is None:
            return None
        else:
            return self.__translate_prev_format(doi_url=doi_url)

    # -- translator --
    def __translate_decode(self, url: str)->str:
        return url.replace('%2F', '/')

    def __translate_prev_format(self, *, doi_url: str)->str:
        """https://dx.doi.org/10.1901%2Fjeab.1976.26-441 からdoiURLを引く。"""
        return self.DOI_STR + doi_url.replace(self.DOI_URL, '')

    # -- model --
    def __find_https_format(self, *, anchor_links: [str])->str or None:
        """取得した全aタグリンクのうち，指定したジャーナルサイトURLに合致するものを検索"""
        results = []
        for link in anchor_links:
            if self.__decision_include_keyword(keyword=self.DOI_URL, text=link):
                results.append(link)
        # print(results)
        if len(results) > 0:
            # print(results[0])
            return results[0]
        else:
            return None

    def __find_network_path_reference_format(self, *, anchor_links: [str])->str or None:
        """取得した全aタグリンクのうち，指定したジャーナルサイトURLに合致するものを検索"""
        # 2017/12/11現在，doiリンクにはネットワークパス参照（http:省略）が使用されている。
        results = []
        for link in anchor_links:
            if self.__decision_include_keyword(keyword=self.DOI_URL_NETWORK_PATH, text=link):
                results.append(link)
        # print(results)
        if len(results) > 0:
            # print(results[0])
            return self.NETWORK_PATH+results[0]
        else:
            return None

    def __decision_include_keyword(self, *, keyword: str, text:str):
        """[text]から[keywordを検索] -> Bool """
        if keyword == '':
            return False
        # print(searchWord in text)
        return keyword in text
