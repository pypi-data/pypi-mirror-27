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
# --- Information ---
# --- Circumstances ---

# === import ===========================================================================================================

""" Standard library """
""" Third party library """
""" Local library """
from getdoi.getArticleURL.getArticleURLController import GetArticleURLControllerImpl
from getdoi.articleinfo.articleInfo import ArticleInfo

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

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


class GetArticleURLControllerStandAloneImpl:
    print('-STAND ALONE MODE- getArticleURLController.py')
    print('Get the article URL for your entered citation.')
    getter = GetArticleURLControllerImpl()
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
                print('1st author: {0}'.format(article_info.first_author))
                print('Main Title: {0}'.format(article_info.article_main_title))
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

# ======================================================================================================================


if __name__ == '__main__':
    main = GetArticleURLControllerStandAloneImpl()
