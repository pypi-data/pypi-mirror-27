#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 translateEscapeSequence.py

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
# --- Circumstances ---

# === import ===========================================================================================================

""" Standard library """
""" Third party library """
""" Local library """

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class TranslateEscapeSequence:
    def escape(self, text: str)->str:
        return text.encode('unicode_escape').decode('utf-8')

    def unescape(self, text: str)->str:
        # /Volumes/RECOVERYUSB/Data\ \(Zebrafish\)/ResistanceToExtPart2/Z156RWF/Z156RWF_76.txt
        # /Volumes/RECOVERYUSB/Data (Zebrafish)/ResistanceToExtPart2/Z156RWF/Z156RWF_76.txt
        return text.replace('\\\\', '__DOUBLE_BACK__').replace('\\', '').replace('__DOUBLE_BACK__', '\\')

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
    print('-STAND ALONE MODE- translateEscapeSequence.py')
    print()
    translator = TranslateEscapeSequence()
    reader = ReadEnteredTextStandAloneImpl()
    while True:
        print('Enter the characters...')
        text = reader.read()
        if text is None:
            # exit
            break
        else:
            print('Escape: {0}'.format(translator.escape(text)))
            print('Unescape: {0}'.format(translator.unescape(text)))
