#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 ioTextFile.py

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
import os
""" Third party library """
""" Local library """

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class IOTextFile:
    # controller
    def open(self, path: str, is_log: bool=True)->[str] or None:
        try:
            opened_file = open(path)
            text_array = opened_file.readlines()  # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
            opened_file.close()
            result = [text.replace('\r', '').replace('\n', '') for text in text_array]
        except:
            if is_log:print('Error! cannot read text file from {0}.'.format(path))
            return None
        return result

    def save(self, contents: str, path: str, file_name: str, is_create_directory: bool=False, is_log: bool=True)->bool:
        if not self.__decision_exist_directory(path):
            if is_create_directory:
                self.__create_directory(path)
            else:
                if is_log:print('Error! cannot find directory at {0}'.format(path))
                return False
        file_path = self.__translate_join_path(path, file_name)
        try:
            opened_file = open(file_path, 'w')
            opened_file.write(contents)
            opened_file.close()
        except:
            if is_log:print('Error! cannot save file for {0}'.format(file_path))
            return False
        if is_log: print('Success to save at {0}.'.format(file_path))
        return True

    def decision_txt_file(self, path: str, is_log: bool=True)->bool:
        if path[-4:] != '.txt':
            if is_log:print('Error! {0} is not match \'.txt\' format.'.format(path))
            return False
        return True

    # translator
    def __translate_join_path(self, directory, folder_name):
        # Join $directory and $folder_name
        # adjusting path delimiter
        DELIMITER = '/'
        result_directory = directory
        result_folder_name = folder_name
        is_directory_delimiter = directory[-1] == DELIMITER
        is_folder_name_delimiter = folder_name[0] == DELIMITER
        # directory[-1] XNOR folder_name[0] then True
        if is_directory_delimiter == is_folder_name_delimiter:
            if is_directory_delimiter == True:
                # remove delimiter
                result_directory = directory[:-1]
            else:
                # add delimiter
                result_directory += DELIMITER
        result = os.path.expanduser(result_directory + result_folder_name)
        return result

    # model
    def __decision_exist_directory(self, path)->bool:
        return os.path.isdir(path)

    def __create_directory(self, directory: str, is_log: bool=True)->bool:
        try:
            os.mkdir(directory)
        except:
            if is_log:print('Error! cannot create directory at {0}'.format(directory))
            return False
        return True

# =============================================================================================================


if __name__ == '__main__':
    print()
