#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 psycnet.py

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


class SSLStateInPsycNET:
    """2017/12/11現在，PsycNETはSSL(https)に対応していない。変更時も動作するようにしておく。"""
    # -- constants --
    PROTOCOLS = ['https://', 'http://']
    __DOI_URL = 'dx.doi.org/'
    __PSYCNET_URL = 'psycnet.apa.org/doi/'

    def get_doi_url(self, url):
        return self.PROTOCOLS[0 if self.__decision_ssl_state(url) else 1]+self.__DOI_URL

    def get_psycnet_url(self, url):
        return self.PROTOCOLS[0 if self.__decision_ssl_state(url) else 1] + self.__PSYCNET_URL

    def __decision_ssl_state(self, url)->bool:
        return self.PROTOCOLS[0] in url


class PsycNET(GettableDOI):
    # -- constants --
    JOURNAL_URL = 'psycnet.apa.org'
    JOURNAL_STR = 'PsychoNET APA'
    DOI_STR = 'doi: '

    # -- controller --
    def get(self, *, url: str)->str or None:
        return self.get_url(url=url)

    def get_url(self, *, url: str)->str or None:
        """return a full URL link"""
        doi_url = self.__find_doi_from_anchor_texts(url=url)
        if doi_url is not None:
            return doi_url

        doi_url = self.__find_doi_from_anchor_links(url=url)
        if doi_url is not None:
            return doi_url

        print('Any DOI found from {journal} ({link})'.format(journal=self.JOURNAL_STR, link=url))
        return None

    def get_prev_format(self, *, url: str)->str or None:
        """doi：[space] [doinumber]"""
        doi_url = self.get_url(url=url)
        if doi_url is not None:
            return self.__translate_prev_format(doi_url=doi_url)
        else:
            return None

    # -- translator --
    def __translate_prev_format(self, *, doi_url: str):
        """https://doi.org/10.1016/1040-8428(93)90007-Q からhttps://doi.org/を引く。"""
        ssl_state = SSLStateInPsycNET()
        return self.DOI_STR+doi_url.replace(ssl_state.get_doi_url(doi_url), '').replace(ssl_state.get_psycnet_url(doi_url), '')

    # -- mdoel --
    def __find_doi_from_anchor_texts(self, url: str):
        """doiをPsycNETから読み込む。doiはanchor_textである。"""
        # e.g. http://psycnet.apa.org/journals/amp/18/8/503/
        # text: http://dx.doi.org/10.1037/h0045185
        soup = BeautifulSoupModelImpl()
        anchor_texts = soup.get_anchor_texts(url)
        ssl_state = SSLStateInPsycNET()
        # print(anchor_links)
        """取得した全anchor_textのうち，http://dx.doi.org/に合致するものを検索"""
        results = []
        if anchor_texts is not None and len(anchor_texts) > 0:
            for link in anchor_texts:
                if ssl_state.get_doi_url(url) in link:
                    results.append(link)
            # print(results)
            if len(results) > 0:
                # print(results[0])
                return results[0]
        print('Any DOI found from anchor-texts from PsycNET ({0})'.format(url))
        return None

    def __find_doi_from_anchor_links(self, url: str):
        """doiをPsycNETから読み込む。doiはanchor_linkである。"""
        # e.g. http://psycnet.apa.org/journals/amp/18/8/503/
        # link: http://psycnet.apa.org/doi/10.1037/h0045185
        soup = BeautifulSoupModelImpl()
        anchor_links = soup.get_anchor_links(url)
        ssl_state = SSLStateInPsycNET()
        # print(anchor_links)
        """取得した全anchor_linkのうち，http://psycnet.apa.org/doi/に合致するものを検索"""
        results = []
        if anchor_links is not None and len(anchor_links) > 0:
            for link in anchor_links:
                if ssl_state.get_psycnet_url(url) in link:
                    results.append(link)
            # print(results)
            if len(results) > 0:
                # print(results[0])
                return results[0]
        print('Any DOI found from anchor-links from PsycNET ({0})'.format(url))
        return None

    def __decision_include_keyword(self, *, keyword: str, text: str):
        """[text]から[keywordを検索] -> Bool """
        if keyword == '':
            return False
        # print(searchWord in text)
        return keyword in text
