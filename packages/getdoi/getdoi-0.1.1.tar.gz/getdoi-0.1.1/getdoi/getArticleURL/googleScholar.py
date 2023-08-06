#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ======================================================================================================

"""
 googleScholar.py

Copyright © 2017 Yuto Mizutani.
This software is released under the MIT License.

Version: 1.0.0

TranslateAuthors: Yuto Mizutani
E-mail: yuto.mizutani.dev@gmail.com
Website: http://operantroom.com

Created: 2017/12/07
Device: MacBook Pro (Retina, 13-inch, Mid 2015)
OS: macOS Serria version 10.12.6
IDE: PyCharm Community Edition 2017.2.4
Python: 3.6.1
"""

# --- References ---
# --- notes ---
# --- Information ---
"""
"""
# --- Circumstances ---
"""
"""

# === import ========================================================================================================

""" Standard library """
""" Third party library """
from articleinfo.articleInfo import ArticleInfo
""" Local library """
from getdoi.getArticleURL.gettableArticleURL import GettableArticleURL
from getdoi.getArticleURL.translateGoogleScholarQuery import TranslateGoogleScholarQuery
from getdoi.scraping.beautifulSoupModel import BeautifulSoupModelImpl

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================


# ======================================================================================================================

class GoogleScholar(GettableArticleURL):
    """
    !! ATTENTION: GoogleScholarには1日20件の制限があります。 !!
    """
    WHITELIST_KEYWORDS_LINK = ['http']
    BLACKLIST_KEYWORDS_SITE_FUNCTIONS = ['accounts.google.com', 'addons']
    BLACKLIST_KEYWORDS_LINK_EXTENSION = ['.pdf']

    def get(self, *, article_info: ArticleInfo)->str or None:
        """
        def get(self, *, article_info: ArticleInfo, num: int)->[str]:
            -- GoogleScholar から論文情報ページまでのURLを取得します。 --
                > GoogleScholarのQueryに第1著者とメインタイトル情報を渡し，検索結果のリンクから引数numだけURLを返します。
                >> 著者とタイトル情報はArticleInfo classから，Query作成はTranslateGoogleScholarQuery classに任せます。

            1. 引数に受け取ったarticle_infoから，第1著者とメインタイトルを抽出します。
            2. 抽出した著者とタイトルから，TranslateGoogleScholarQueryによりGoogleScholar用のQueryを含んだURLに変換します。
            3. GoogleScholar URLをスクレイピングし，リストに保持します。
            4. 結果として引数numの数だけ返します。
        """

        first_author = article_info.first_author
        main_title = article_info.article_main_title
        translator = TranslateGoogleScholarQuery()
        scholar_url = translator.translate(first_author, main_title)
        soup = BeautifulSoupModelImpl()
        anchor_texts_and_links = soup.get_anchor_texts_and_links(scholar_url)

        # [['text', 'link'], ['text', 'link']]
        # print(anchor_texts_and_links)

        results_urls = self.__whitelisted_texts_and_links(anchor_texts_and_links, self.WHITELIST_KEYWORDS_LINK)
        results_without_site_funcs = self.__blacklisted_texts_and_links(results_urls, self.BLACKLIST_KEYWORDS_SITE_FUNCTIONS)
        results_without_pdfs = self.__blacklisted_texts_and_links(results_without_site_funcs, self.BLACKLIST_KEYWORDS_LINK_EXTENSION, True)
        cooked_results = results_without_pdfs

        return self.__decision_title_match_link(cooked_results, main_title)

    def __whitelisted_texts_and_links(self, results: [str], keywords: [str], is_search_or: bool=True)->[str]:
        """keywordsに合致する要素のみ抽出する。is_search_orはFalseでand検索。"""
        cooked_results = []
        for result in results:
            is_add = not is_search_or
            for keyword in keywords:
                if keyword in result[1]:
                    is_add = is_search_or
            if is_add:
                cooked_results.append(result)
        return cooked_results

    def __blacklisted_texts_and_links(self, results: [str], keywords: [str], is_search_last: bool=False)->[str]:
        """keywordsに合致しない要素のみ抽出する。is_search_lastはTrueで拡張子探索用の後方検索。"""
        cooked_results = []
        for result in results:
            is_add = True
            for keyword in keywords:
                if is_search_last:
                    if len(result[1]) > len(keyword) and result[1][-len(keyword):] == keyword:
                        is_add = False
                        break
                else:
                    if keyword in result[1]:
                        is_add = False
                        break
            if is_add:
                cooked_results.append(result)
        return cooked_results

    def __decision_title_match_link(self, results: [[str]], title: str)->str or None:
        """
        [['text', 'link'], ['text', 'link']]から，textにタイトルがあるので，そのタイトルとの一致度を比較する。
            > CRITERION以上ならそのリンクを返す。
        """
        CRITERION = 0.5
        if len(results) < 1:
            return None
        for result in results:
            result_text = result[0]
            result_link = result[1]

            point = 0
            length = len(title.split())
            for separated_title in title.split():
                if separated_title in result_text:
                    point += 1
            # print(point/length)
            if (point/length) >= CRITERION:
                return result_link
        return None


    # def __whitelisted(self, results: [str], keywords: [str], is_search_or: bool=True)->[str]:
    #     """keywordsに合致する要素のみ抽出する。is_search_orはFalseでand検索。"""
    #     cooked_results = []
    #     for result in results:
    #         is_add = not is_search_or
    #         for keyword in keywords:
    #             if keyword in result:
    #                 is_add = is_search_or
    #         if is_add:
    #             cooked_results.append(result)
    #     return cooked_results
    #
    # def __blacklisted(self, results: [str], keywords: [str], is_search_last: bool=False)->[str]:
    #     """keywordsに合致しない要素のみ抽出する。is_search_lastはTrueで拡張子探索用の後方検索。"""
    #     cooked_results = []
    #     for result in results:
    #         is_add = True
    #         for keyword in keywords:
    #             if is_search_last:
    #                 if len(result) > len(keyword) and result[-len(keyword):] == keyword:
    #                     is_add = False
    #                     break
    #             else:
    #                 if keyword in result:
    #                     is_add = False
    #                     break
    #         if is_add:
    #             cooked_results.append(result)
    #     return cooked_results


# ======================================================================================================================

class ReadEnteredTextStandAloneImpl:
    """ If user display_input, drop filesPath then return files, exit then return None """
    # -- variables --
    __display_input_text = '> '
    __display_output_text = '>> Read: '

    # reader = ReadEnteredTextStandAloneImpl()
    # while True:
    #     print()
    #     print('Enter the characters...')
    #     text = reader.read()
    #     if text is None:
    #         # exit
    #         break

    def read(self) -> str or None:
        entered_str = input(self.__display_input_text)
        if self.__decision_exit(entered_str):
            # if user display_inputs exit meaning then exit
            return None
        else:
            print('{0}{1}'.format(self.__display_output_text, entered_str))
            return entered_str

    def __decision_exit(self, text) -> bool:
        # -- constants --
        EXIT_TEXTS = ['e', '-e', 'exit', 'exit()', 'Exit', 'Exit()']
        # decision match strings argument and EXIT_TEXTS
        for exit_text in EXIT_TEXTS:
            if text == exit_text:
                return True
        return False

# ======================================================================================================================


if __name__ == '__main__':
    print('-STAND ALONE MODE- googleScholar.py')
    print('Get the article URL for your entered citation.')
    getter = GoogleScholar()
    reader = ReadEnteredTextStandAloneImpl()
    # Kuroda, T., Mizutani, Y., Cançado, C. R., & Podlesnik, C. A. (2017). Operant models of relapse in zebrafish (Danio rerio): Resurgence, renewal, and reinstatement. Behavioural brain research, 335, 215-222.
    # Kuroda, T.
    # Operant models of relapse in zebrafish (Danio rerio).
    while True:
        print()
        print('Enter the first author...')
        first_author = reader.read()
        if first_author is None:
            # exit
            break
        else:
            print()
            print('Enter the article main title...')
            main_title = reader.read()
            if main_title is None:
                # exit
                break
            else:
                article_info = ArticleInfo()
                article_info.first_author = first_author
                article_info.article_main_title = main_title
                translator = TranslateGoogleScholarQuery()
                scholar_url = translator.translate(article_info.first_author, article_info.article_main_title)
                print('1st author: {0}'.format(article_info.first_author))
                print('Main Title: {0}'.format(article_info.article_main_title))
                print('Scholar URL: {0}'.format(scholar_url))
                print()
                print('Proceed (y/n)?')
                proceed = reader.read()
                if proceed is None or proceed == 'n':
                    # exit
                    break
                elif proceed == 'y':
                    result = getter.get(article_info=article_info)
                    print('Article URL: {0}'.format(result))
                else:
                    print('Your response ({0}) was not one of the expected responses: y, n'.format(proceed))

