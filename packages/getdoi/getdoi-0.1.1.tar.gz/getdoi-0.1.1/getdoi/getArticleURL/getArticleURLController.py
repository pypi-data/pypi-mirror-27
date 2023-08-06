#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 getArticleURLController.py

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
"""
[fleshler hoffman]
https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=fleshler+hoffman&oq=Fleshler
[author:fleshler hoffman]
https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=author%3Afleshler+hoffman&btnG=
"""
# --- Information ---
# --- Circumstances ---

# === import ===========================================================================================================

""" Standard library """
from enum import Enum
""" Third party library """
from articleinfo.articleInfo import ArticleInfo
""" Local library """
from getdoi.getArticleURL.gettableArticleURL import GettableArticleURL
from getdoi.getArticleURL.googleScholar import GoogleScholar


# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================


# ======================================================================================================================


class SearchType(Enum):
    GOOGLE_SCHOLAR = GoogleScholar


class GetArticleURLControllerImpl(GettableArticleURL):
    # -- variables --
    search_impl = GettableArticleURL

    # -- controller --
    def get(self, *, article_info: ArticleInfo)->str or None:
        # site = GoogleScholar()
        # result = site.get(article_info=article_info)
        # return result
        search_type = self.get_search_type()
        if search_type is None:
            return None
        search_impl = search_type.value()
        if search_impl is not None:
            info = search_impl.get(article_info=article_info)
            return info
        else:
            return None

    def get_search_type(self):
        # FIX (自動で検索サイトを特定する必要はない？取得失敗で変更？)
        for type in SearchType:
            # FIX: add
            if True:
                self.print_search_type(type)
                return type
        print('get_search_type(): no match search site')
        return None

    def print_search_type(self, type: SearchType):
        type_str = ''
        if type == SearchType.GOOGLE_SCHOLAR:
            type_str = 'Google Scholar'
        print('Search site: {0}'.format(type_str))

    def __decision_include_keyword(self, *, keyword: str, text: str) -> bool:
        """[text]から[keywordを検索] -> Bool """
        if keyword == '':
            return False
        # print(searchWord in text)
        return keyword in text


# ======================================================================================================================
