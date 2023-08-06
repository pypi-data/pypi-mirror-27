#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 plos.py

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


class PLOS(GettableDOI):
    # -- constants --
    JOURNAL_URL = 'journals.plos.org'
    JOURNAL_STR = 'PLOS'
    DOI_KEY = "http://journals.plos.org/plosgenetics/article?id="
    DOI_URL = 'https://doi.org/'
    DOI_STR = 'doi: '

    # -- controller --
    def get(self, *, url: str)->str or None:
        return self.get_url(url=url)

    def get_url(self, *, url: str)->str or None:
        raw_doi = self.__get_raw_doi(url=url)
        if raw_doi is not None:
            return self.__translate_url_format(raw_doi=raw_doi)

        doi_url = self.__find_doi_url_from_anchor_texts(url=url)
        if doi_url is not None:
            return doi_url

        doi_url = self.__find_doi_url_from_anchor_links(url=url)
        if doi_url is not None:
            return doi_url

        print('Any DOI found from PLOS ({0})'.format(url))
        return None

    def get_prev_format(self, *, url: str)->str or None:
        raw_doi = self.__get_raw_doi(url=url)
        if raw_doi is not None:
            return self.__translate_prev_format(doi_url=raw_doi)

        doi_url = self.__find_doi_url_from_anchor_texts(url=url)
        if doi_url is not None:
            return self.__translate_prev_format(doi_url=doi_url)

        doi_url = self.__find_doi_url_from_anchor_links(url=url)
        if doi_url is not None:
            return self.__translate_prev_format(doi_url=doi_url)

        print('Any DOI found from PLOS ({0})'.format(url))
        return None


    # -- translator --
    def __translate_url_format(self, *, raw_doi: str)->str:
        """10.1371/journal.pgen.0010066 に https://doi.org/ を加える。"""
        return self.DOI_URL+raw_doi

    def __translate_prev_format(self, *, doi_url: str)->str:
        """https://doi.org/10.1371/journal.pgen.0010066 にhttps://doi.org/を除き doi: を加える。"""
        return self.DOI_STR + doi_url.replace(self.DOI_URL, '')

    # -- model --
    def __get_raw_doi(self, *, url: str)->str or None:
        """doiをPLOSから読み込む。が，PLOSは元々doiがURLに含まれている。"""
        # e.g. http://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.0010066
        # 10.1371/journal.pgen.0010066
        if self.__decision_include_keyword(keyword=self.DOI_KEY, text=url):
            num = url.find(self.DOI_KEY)
            count = 0
            doi = ""
            for char in url:
                if count >= num + len(self.DOI_KEY):
                    doi += char
                count += 1
            # 10.1371/journal.pgen.0010066
            # print(doi)
            return doi
        else:
            return None

    def __find_doi_url_from_anchor_links(self, *, url: str)->str or None:
            soup = BeautifulSoupModelImpl()
            anchor_links = soup.get_anchor_links(url)
            # print(anchor_links)
            """取得したanchor_linksのうち，DOI_KEYに合致するものを検索"""
            results = []
            for link in anchor_links:
                if self.__decision_include_keyword(keyword=self.DOI_KEY, text=link):
                    results.append(link)
            # print(results)
            """https://doi.org/10.1371/journal.pgen.0010066"""
            if len(results) > 0:
                print(results[0])
                return results[0]
            else:
                return None

    def __find_doi_url_from_anchor_texts(self, *, url: str)->str or None:
            soup = BeautifulSoupModelImpl()
            anchor_texts = soup.get_anchor_texts(url)
            # print(anchor_texts)
            """取得したanchor_textsのうち，DOI_KEYに合致するものを検索"""
            results = []
            for link in anchor_texts:
                if self.__decision_include_keyword(keyword=self.DOI_KEY, text=link):
                    results.append(link)
            # print(results)
            """https://doi.org/10.1371/journal.pgen.0010066"""
            if len(results) > 0:
                print(results[0])
                return results[0]
            else:
                return None

    def __decision_include_keyword(self, *, keyword, text):
        """[text]から[keywordを検索] -> Bool """
        if keyword == '':
            return False
        # print(searchWord in text)
        return keyword in text
