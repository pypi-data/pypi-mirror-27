#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 __init__.py

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
import sys
import os
import time
""" Third party library """
from articleinfo.getArticleInfoFromCitation.getArticleInfoFromCitationController import GetArticleInfoFromCitationControllerImpl
""" Local library """
from getdoi.reader.readEnteredText import ReadEnteredTextImpl
from getdoi.reader.ioTextFile import IOTextFile
from getdoi.translator.translateEscapeSequence import TranslateEscapeSequence
from getdoi.getArticleURL.getArticleURLController import GetArticleURLControllerImpl
from getdoi.getDOIFromURL.getDOIFromURLController import GetDOIFromURLControllerImpl

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

__version__ = '0.1.0'
__author__ = 'Yuto Mizutani (yuto.mizutani.dev@gmail.com)'
__copyright__ = 'Copyright (c) 2017 Yuto Mizutani'
__license__ = 'MIT'
__all__ = ['']

# ======================================================================================================================



class Main:
    #### init
    def __init__(self, arguments: [str]=None):
        self.copyright()
        self.instractions()
        self.notice()
        self.__controller_select_work(arguments)

    #### display notes
    def copyright(self):
        print('getdoi - python3')
        print('Copyright © 2017 Yuto Mizutani.')
        print('This software is released under the MIT License.')
        print()

    def instractions(self):
        print('This software entered article\'s citation text and display doi.')
        print()

    def notice(self):
        print('NOTICE')
        print(' This software is pre-alpha version now.')
        print(' You can enter APA style format only at the moment.')
        print(' This software can search from only Google Scholar at the moment.')
        print()
        print('ATTENTION!!')
        print(' This software searches article URL using Google Scholar.')
        print(' Google Scholar search request limit several dozen in short time. It could be an error if you try many times.')
        print()

    #### controller
    def __controller_select_work(self, arguments: [str]=None):
        # 起動時の引数の有無で読み込みかターミナル起動か変更する。
        if arguments is not None:
            self.__controller_work_using_arguments(arguments)
        else:
            self.__controller_work_on_terminal()

    def __controller_work_using_arguments(self, arguments: [str]=None):
        if arguments is None or len(arguments) < 1:
            print('Error! Arguments are invalid.')
            return
        for argv in arguments:
            argv = self.__translate_blanks(argv)
            self.__controller_get_doi(argv)

    def __controller_work_on_terminal(self):
        reader = ReadEnteredTextImpl(
            display_input_instructions='Enter the citation format, article URL or the .txt file path written in it...'
        )
        while True:
            print()
            read_text = reader.read()
            if read_text is None:
                # exit
                break
            else:
                if read_text == '' or len(read_text) < 1:
                    print('Entered text is null or empty!')
                else:
                    self.__controller_get_doi(read_text)

    def __controller_get_doi(self, argv: str):
        if self.__decision_is_file_path(argv):
            if self.__decision_is_txt_file(argv):
                escaper = TranslateEscapeSequence()
                path = escaper.unescape(argv)
                self.__usecase_get_doi_using_txt_file(path)
            else:
                print('Error! Path: \"{0}\" is invalid.'.format(argv))
        else:
            self.__usecase_select_work(content=argv)

    #### usecase
    def __usecase_select_work(self, content: str=None, is_confirm: bool=True):
        # contentがhttpから始まればscholarまたはarticleを探す。合致しなければcitationとして扱う。
        if content is None or content == '':
            print('Error! no content!')
            return
        elif self.__decision_include_keyword(keyword='http', text=content):
            print('Entered type: URL')
            url = self.__translate_blanks(content)
            # decision search URL
            # QUESTIONS: citation情報がないままsearchURLからDOIのみ持ってくる意味はあるのか？
            #               -> 現状では不要と判断。
            # decision article URL
            getter_doi = GetDOIFromURLControllerImpl()
            if getter_doi.get_journal_type(url=url, is_silent=True):
                self.__usecase_get_doi_using_article_url('(You Inputted URL)', url, is_confirm)
                return
            else:
                print('Could not find URL processing...')
        else:
            print('Entered type: citation')
            self.__usecase_get_doi_using_citation(citation=content, is_confirm=is_confirm)

    def __usecase_get_doi_using_txt_file(self, path: str):
        io = IOTextFile()
        if io.decision_txt_file(path):
            contents = io.open(path)
            for content in contents:
                self.__usecase_select_work(content, is_confirm=False)

    def __usecase_get_doi_using_citation(self, citation: str, is_confirm: bool=True):
        print('>> {0}'.format(citation))
        article_info_getter = GetArticleInfoFromCitationControllerImpl()
        article_info = article_info_getter.get_all(citation=citation)
        if article_info is None:
            print('Failed! Could not find article informations from citation...')
            print('Citation: {0}'.format(citation))
            return
        if article_info.doi != '':
            print('Successfully found DOI!')
            print('DOI: {0}'.format(article_info.doi))
            print()
            print(citation)
        print('First author: {0}'.format(article_info.first_author))
        print('Main title: {0}'.format(article_info.article_main_title))
        if is_confirm and not self.__proceed():
                return
        article_url_getter = GetArticleURLControllerImpl()
        article_url = article_url_getter.get(article_info=article_info)
        if article_url == '':
            print('Failed! Could not find article URL from citation...')
            print('First author: {0}'.format(article_info.first_author))
            print('Main title: {0}'.format(article_info.article_main_title))
            return
        if is_confirm and not self.__proceed():
                return
        self.__usecase_get_doi_using_article_url(citation, article_url, is_confirm)

    def __usecase_get_doi_using_article_url(self, citation: str, article_url: str, is_confirm: bool=True):
        print('Article URL: {0}'.format(article_url))
        doi_getter = GetDOIFromURLControllerImpl()
        doi = doi_getter.get_url(url=article_url)
        if doi is None:
            print('Failed! Could not find DOI from URL...')
            print('Article URL: '.format(article_url))
            return
        print('Found DOI!')
        print('DOI: {0}'.format(doi))
        print('Citation include doi:')
        print(citation + ' ' + doi)
        print()
        # wait 60-s
        print('============  wait 60 seconds =====================================================================')
        time.sleep(60.0)

    #### translator
    def __translate_blanks(self, text: str)->str:
        while text[0] == ' ':
            text = text[1:]
        while text[-1] == ' ':
            text = text[:-1]
        return text

    #### model
    def __proceed(self)->bool or None:
        reader = ReadEnteredTextImpl(display_input_instructions=False)
        while True:
            print()
            print('Proceed (y/n)?')
            proceed = reader.read()
            if proceed is None:
                return None
            if proceed == 'n':
                return False
            if proceed == 'y':
                return True
            else:
                print('Your response ({0}) was not one of the expected responses: y, n'.format(proceed))

    def __decision_is_file_path(self, argv: str)->bool:
        def linux()->bool:
            return os.name == 'posix' and argv[0] == '/'
        def windows()->bool:
            return os.name == 'nt' and (':¥' in argv or ':\\' in argv)
        return linux() or windows()

    def __decision_is_txt_file(self, path: str)->bool:
        return '.' in path and path.split('.')[-1] == 'txt'

    def __decision_include_keyword(self, *, keyword: str, text: str) -> bool:
        """[text]から[keywordを検索] -> Bool """
        if keyword == '':
            return False
        # print(searchWord in text)
        return keyword in text

# ======================================================================================================================


if __name__ == '__main__':
    # /Users/ym/Downloads/Untitled.txt
    # get arguments
    arguments = sys.argv
    # If it has arguments then get DOI using the arguments
    if len(arguments) > 1:
        main = Main(arguments[1:-1])
    # In most cases, work on Terminal
    else:
        main = Main()
