#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 articleInfo.py

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

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class ArticleInfo:
    # -- variables --
    authors = [str]
    first_author = str
    year = str
    article_title = str
    article_main_title = str
    article_sub_title = str
    journal_title = str
    volume = str
    issue = str
    pages = [str]  # [Start, End] or [Start]
    doi = str

    def print(self):
        print('1st author: {0}'.format(self.first_author))
        print('Authors: {0}'.format(self.authors))
        print('Year: {0}'.format(self.year))
        print('Title: {0}'.format(self.article_title))
        print('Main Title: {0}'.format(self.article_main_title))
        print('Sub title: {0}'.format(self.article_sub_title))
        print('Journal: {0}'.format(self.journal_title))
        print('Volume: {0}'.format(self.volume))
        print('Issue: {0}'.format(self.issue))
        print('Pages: {0}'.format(self.pages))
        print('DOI: {0}'.format(self.doi))

    def nill_check(self):
        if self.authors is None: self.authors = ['']
        if self.first_author is None: self.first_author = ''
        if self.year is None: self.year = ''
        if self.article_title is None: self.article_title = ''
        if self.article_main_title is None: self.article_main_title = ''
        if self.article_sub_title is None: self.article_sub_title = ''
        if self.journal_title is None: self.journal_title = ''
        if self.volume is None: self.volume = ''
        if self.issue is None: self.issue = ''
        if self.pages is None: self.pages = ['']
        if self.doi is None: self.doi = ''
