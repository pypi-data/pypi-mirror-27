#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 gettableDOI.py

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
from articleinfo.articleInfo import ArticleInfo

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class GettableArticleInfo(object):
    def get_all(self, *, citation: str)->ArticleInfo or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_authors(self, *, citation: str)->[str] or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_first_author(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_year(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_article_title(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_article_main_title(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_article_sub_title(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_journal_title(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_volume(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_issue(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_pages(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError

    def get_doi(self, *, citation: str)->str or None:
        print('Error! Can not call protocol funcs!')
        raise RuntimeError
