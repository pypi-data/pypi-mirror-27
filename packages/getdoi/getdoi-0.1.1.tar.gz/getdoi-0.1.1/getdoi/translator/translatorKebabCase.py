#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ======================================================================================================

"""
 translatorKebabCase.py

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
""" Local library """

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# =============================================================================================================


class TranslatorKebabCaseImpl:
    def translate(self, text)->str:
        # e.g. ABASingle-CaseDesign
        # >> aba-single-case-design
        text = text.replace('--', '-').replace(' ', '-').replace('--', '-').replace('_', '-').replace('--', '-')
        i = 0
        while i < len(text):
            # > ABASingle-CaseDesign
            if i != 0 and text[i] != text[-1] and text[i] != text[i].lower() and text[i+1] != text[i+1].upper():
                text = (text[:i] + '-' + text[i:]).replace('--', '-')
                i += 1
            if i != 0 and text[i] != text[-1] and text[i] != text[i].lower() and text[i-1] != text[i-1].upper():
                text = (text[:i] + '-' + text[i:]).replace('--', '-')
                i += 1
            i += 1
        if text[0] == '-':
            text = text[1:]
        # > ABA-Single-Case-Design
        text = text.lower()
        # > aba-single-case-designaABASingle-CaseDesign
        return text

# ======================================================================================================================


class ReadEnteredTextStandAloneImpl:
    """ If user display_input, drop filesPath then return files, exit then return None """
    # -- variables --
    __display_input_instructions = 'Enter the characters...'
    __display_input_text = '> '
    __display_output_text = '>> Read: '

    # reader = ReadEnteredTextStandAloneImpl()
    # while True:
    #     text = reader.read()
    #     if text is None:
    #         # exit
    #         break

    def read(self)->str or None:
        print(self.__display_input_instructions)
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
    print('-STAND ALONE MODE- translatorKebabCase.py')
    print()
    translator = TranslatorKebabCaseImpl()
    reader = ReadEnteredTextStandAloneImpl()
    while True:
        text = reader.read()
        if text is None:
            # exit
            break
        else:
            print(translator.translate(text))
