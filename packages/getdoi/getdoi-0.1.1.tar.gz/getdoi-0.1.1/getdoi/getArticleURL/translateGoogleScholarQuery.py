#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 translateGoogleScholarQuery.py

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
"""
[Scholar query]
https://www.google.co.jp/intl/ja/scholar/refinesearch.html

[urllib parse]
https://qiita.com/yagays/items/e59731b3930252b5f0c4
https://torina.top/detail/305/

[URL encode/decode]
http://www.lifewithpython.com/2016/07/python-url-encode-decode.html
http://www.seil.jp/doc/index.html#tool/url-encode.html

[try query]
https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=intitle%3A%22The+zebrafish+reference+genome+sequence+and+its+relationship+to+the+human+genome%22&btnG=
"""
# --- notes ---
"""
著者クエリ: author:"mizutani y"
タイトルクエリ: intitle:"title"
"""
# --- Information ---
# --- Circumstances ---

# === import ===========================================================================================================

""" Standard library """
""" Third party library """
import urllib.parse
import urllib
""" Local library """

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class TranslateGoogleScholarQuery:
    # https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=intitle%3A%22The+zebrafish+reference+genome+sequence+and+its+relationship+to+the+human+genome%22&btnG=
    # https://scholar.google.com/scholar?q=intitle%3A%22The+zebrafish+reference+genome+sequence+and+its+relationship+to+the+human+genome%22
    SCHOLAR_URL = 'https://scholar.google.com/scholar'

    def translate(self, first_author: (str or None)=None, title: (str or None)=None)->str or None:
        if first_author is None and title is None:
            print('Error! class TranslatorScholarQuery:def translate() arg is invalid!')
            return None
        else:
            query = self.__get_query(first_author, title)
            return self.SCHOLAR_URL + ('?' if query != '' else '') + query

    def __get_query(self, first_author: str, title: str)->str:
        query_key = 'q='
        author_query = self.__translate_query_author(first_author)
        conjunction_query = '+' if (first_author != title) and title is not None else ''
        title_query = self.__translate_query_title(title)
        return query_key + author_query + conjunction_query + title_query

    def __translate_query_author(self, first_author: str or None):
        # Fleshler, M.
        # > author:"fleshler m"
        if first_author is None or first_author == '':
            return ''
        return urllib.parse.quote(
            'author:\"'+(first_author.replace('.', '').replace(',', '').replace(' ', '+')).lower()+'\"',
            safe='+'
        )

    def __translate_query_title(self, title: str):
        # A progression for generating variable-interval schedules.
        # > intitle:"A progression for generating variable-interval schedules."
        if title is None or title == '':
            return ''
        return urllib.parse.quote('intitle:\"'+title.replace(' ', '+')+'\"', safe='+')

# ======================================================================================================================


class ReadEnteredTextStandAloneImpl:
    """ If user display_input, drop filesPath then return files, exit then return None """
    # -- variables --
    __display_input_text = '> '
    __display_output_text = '>> Read: '

    # reader = ReadEnteredTextStandAloneImpl()
    # while True:
    #     text = reader.read()
    #     if text is None:
    #         # exit
    #         break

    def read(self)->str or None:
        entered_str = input(self.__display_input_text)
        if self.__decision_exit(entered_str):
            # if user display_inputs exit meaning then exit
            return None
        else:
            print('{0}{1}'.format(self.__display_output_text, entered_str))
            return entered_str

    def __decision_exit(self, text)->bool:
        # -- constants --
        EXIT_TEXTS = ['e', '-e', 'exit', 'exit()', 'Exit', 'Exit()']
        # decision match strings argument and EXIT_TEXTS
        for exit_text in EXIT_TEXTS:
            if text == exit_text:
                return True
        return False

# ======================================================================================================================


if __name__ == '__main__':
    print('-STAND ALONE MODE- translateGoogleScholarQuery.py')
    translator = TranslateGoogleScholarQuery()
    reader = ReadEnteredTextStandAloneImpl()
    while True:
        print()
        print('Enter the first author...')
        first_author = reader.read()
        print('Enter the title...')
        title = reader.read()
        if first_author is None or title is None:
            # exit
            break
        else:
            print(translator.translate(first_author, title))
