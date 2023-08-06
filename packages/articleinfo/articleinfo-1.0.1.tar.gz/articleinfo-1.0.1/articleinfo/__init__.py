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
"""
<package>
https://www.slideshare.net/kei10in/python-package-constructure
<github>
https://qiita.com/under_chilchil/items/ec9d0050c1e3fb6576de
<folder sample>
https://github.com/getanewsletter/BeautifulSoup4
https://github.com/pypa/pip
<setup>
https://pypi.python.org/pypi?%3Aaction=list_classifiers
"""
# --- notes ---
# --- Information ---
# --- Circumstances ---

# === import ===========================================================================================================

""" Standard library """
""" Third party library """
""" Local library """
from articleinfo.getArticleInfoFromCitation.getArticleInfoFromCitationController import GetArticleInfoFromCitationControllerStandAloneImpl

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

__version__ = '0.1.0'
__author__ = 'Yuto Mizutani (yuto.mizutani.dev@gmail.com)'
__copyright__ = 'Copyright (c) 2017 Yuto Mizutani'
__license__ = 'MIT'
__all__ = ['']

# ======================================================================================================================

if __name__ == '__main__':
    main = GetArticleInfoFromCitationControllerStandAloneImpl()
