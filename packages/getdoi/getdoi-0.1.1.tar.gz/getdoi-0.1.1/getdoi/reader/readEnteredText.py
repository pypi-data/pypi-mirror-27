#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 readEnteredText.py

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


class ReadEnteredTextImpl:
    """ If user display_input, drop filesPath then return files, exit then return None """
    # -- constants --
    EXIT_TEXTS = ['e', '-e', 'exit', 'exit()', 'Exit', 'Exit()']
    # -- variables --
    __display_input_instructions = 'Enter the characters...'
    __display_input_text = '> '
    __display_output_text = '>> Read: '

    def __init__(self, display_input_instructions=None, display_input_text=None, display_output_text=None):
        # None:Default text, (Any text):Change text, False:No display_output
        if display_input_instructions is not None:
            self.__display_input_instructions = display_input_instructions
        if display_input_text is not None:
            self.__display_input_text = display_input_text
        if display_output_text is not None:
            self.__display_output_text = display_output_text

    def read(self)->str or None:
        """ If user display_input, drop filesPath then return files, exit then return None """
        if self.__display_input_instructions is not False:
            print(self.__display_input_instructions)
        if self.__display_input_text is False:
            self.__display_input_text = ''
        entered_str = input(self.__display_input_text)
        if self.__decision_exit(entered_str):
            # if user display_inputs exit meaning then exit
            return None
        else:
            if self.__display_output_text is not False:
                print('{0}{1}'.format(self.__display_output_text, entered_str))
            return entered_str

    def __decision_exit(self, text)->bool:
        # decision match strings argument and EXIT_TEXTS
        for exit_text in self.EXIT_TEXTS:
            if text == exit_text:
                return True
        return False

# ======================================================================================================================


if __name__ == '__main__':
    print('-STAND ALONE MODE- readEnteredText.py')
    print()
    main = ReadEnteredTextImpl()
    while True:
        text = main.read()
        if text is None:
            # exit
            break
