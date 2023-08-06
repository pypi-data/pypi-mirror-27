#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 getDOIFromURLControllerStandAlone.py

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
from getdoi.getDOIFromURL.getDOIFromURLController import GetDOIFromURLControllerImpl

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


class GetDOIFromURLControllerStandAloneImpl:
    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1404199/
    # -- variables --
    is_help = True
    is_state = True
    controller = GetDOIFromURLControllerImpl
    reader = ReadEnteredTextStandAloneImpl

    # -- init --
    def __init__(self):
        print('-STAND ALONE MODE- getDOIFromURLController.py')
        self.controller = GetDOIFromURLControllerImpl()
        self.reader = ReadEnteredTextStandAloneImpl()
        self.loop()

    def loop(self):
        while True:
            print()
            print('Enter the journal URL...')
            if self.is_help:
                print('... (URL)   : {0}'.format('DOI full link' if self.is_state else 'DOI previous format (doi: xxxx)'))
                print('... -l (URL): DOI full link')
                print('... -p (URL): DOI previous format (doi:[space] [doinumber])')
                print('... -c      : Change state')
                print('... -h      : Hide help')
            text = self.reader.read()
            if text is None:
                # exit
                break
            else:
                if text == '':
                    print('Entered text is null or empty!')
                    continue
                while text[0] == ' ':
                    text = text[1:]
                while text[-1] == ' ':
                    text = text[:-1]
                # print(text)

                if text == 'c' or text[0:2] == '-c':
                    print('Change state!')
                    self.is_state = not self.is_state
                    continue

                if text == 'h' or text[0:2] == '-h':
                    print('Hide help!')
                    self.is_help = not self.is_help
                    continue

                elif text[0:3] == '-p ':
                    url = text[3:]
                    if 'http' in url:
                        doi_prev = self.controller.get_prev_format(url=url)
                        print('URL: {0}'.format(url))
                        print('DOI: {0}'.format(doi_prev))
                    else:
                        print('Error! URL is invalid.')
                    continue

                elif text[0:3] == '-l ':
                    url = text[3:]
                    if 'http' in url:
                        doi_link = self.controller.get_url(url=url)
                        print('URL: {0}'.format(url))
                        print('DOI: {0}'.format(doi_link))
                    else:
                        print('Error! URL is invalid.')
                    continue

                else:
                    if 'http' in text:
                        doi_link = self.controller.get(url=text)
                        print('URL: {0}'.format(text))
                        print('DOI: {0}'.format(doi_link))
                    else:
                        print('Error! URL is invalid.')
                    continue

# ======================================================================================================================


if __name__ == '__main__':
    main = GetDOIFromURLControllerStandAloneImpl()
