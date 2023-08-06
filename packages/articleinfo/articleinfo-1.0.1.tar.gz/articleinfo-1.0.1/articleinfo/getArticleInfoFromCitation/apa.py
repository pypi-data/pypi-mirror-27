#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ======================================================================================================

"""
 apa.py

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
from .gettableArticleInfo import GettableArticleInfo
from articleinfo.articleInfo import ArticleInfo

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================


# ======================================================================================================================

class APA(GettableArticleInfo):
    # https://web.williams.edu/wp-etc/acad-resources/survival_guide/CitingDoc/APA1.php

    # Journal Article
    # Author's Last Name, First Initial. Middle Initial. (Year).
    # Article title.
    # Journal Title, Volume Number (Issue Number), Page Numbers. DOI

    # Citations:
    # Schooler, D. (2008).
    # Real women have curves: A longitudinal investigation of TV and the body image development of Latina adolescents.
    # Journal of Adolescent Research, 23, 132-153. doi:10.1177/0743558407310712

    def get_all(self, *, citation: str)->ArticleInfo or None:
        article_info = ArticleInfo()
        article_info.first_author = self.get_first_author(citation=citation)
        article_info.authors = self.get_authors(citation=citation)
        article_info.year = self.get_year(citation=citation)
        article_info.article_title = self.get_article_title(citation=citation)
        article_info.article_main_title = self.get_article_main_title(citation=citation)
        article_info.article_sub_title = self.get_article_sub_title(citation=citation)
        article_info.journal_title = self.get_journal_title(citation=citation)
        article_info.volume = self.get_volume(citation=citation)
        article_info.issue = self.get_issue(citation=citation)
        article_info.pages = self.get_pages(citation=citation)
        article_info.doi = self.get_doi(citation=citation)
        article_info.nill_check()
        return article_info

    def get_authors(self, *, citation: str)->[str] or None:
        authors_text = citation.split('. (')[0].replace('& ', '').replace('... ', '')
        return [author_text+'.' for author_text in authors_text.split('., ')]

    def get_first_author(self, *, citation: str)->str or None:
        return self.get_authors(citation=citation)[0]

    def get_year(self, *, citation: str)->str or None:
        return citation.split('. (')[1].split('). ')[0] if len(citation.split('. (')) > 1 else None

    def get_article_title(self, *, citation: str)->str or None:
        return '. '.join(', '.join(citation[citation.find('). ')+len('). '):].split(', ')[0:-2]).split('. ')[0:-1])+'.'

    def get_article_main_title(self, *, citation: str)->str or None:
        all_title_text = '. '.join(', '.join(citation[citation.find('). ')+len('). '):].split(', ')[0:-2]).split('. ')[0:-1])+'.'
        return all_title_text.split(': ')[0]+'.' if len(all_title_text.split(': ')) >= 2 else all_title_text

    def get_article_sub_title(self, *, citation: str)->str or None:
        all_title_text = '. '.join(', '.join(citation[citation.find('). ')+len('). '):].split(', ')[0:-2]).split('. ')[0:-1])+'.'
        return all_title_text.split(': ')[-1] if len(all_title_text.split(': ')) >= 2 else None

    def get_journal_title(self, *, citation: str)->str or None:
        return citation.split(', ')[-3].split('. ')[-1]

    def get_volume(self, *, citation: str)->str or None:
        volume_and_issue = citation.split(', ')[-2] if len(citation.split(', ')) > 1 else None
        if volume_and_issue is None:
            return None
        return volume_and_issue.split('(')[0] if len(volume_and_issue.split('(')) > 1 else volume_and_issue.split(',')[0]

    def get_issue(self, *, citation: str)->str or None:
        volume_and_issue = citation.split(', ')[-2] if len(citation.split(', ')) > 1 else None
        if volume_and_issue is None:
            return None
        return volume_and_issue.split('(')[-1].replace(')', '') if len(volume_and_issue.split('(')) > 1 else None

    def get_pages(self, *, citation: str)->str or None:
        return citation.split(', ')[-1].split('.')[0].split('-')

    def get_doi(self, *, citation: str)->str or None:
        if len(citation.split('doi:')) > 1:
            doi_str = citation.split('doi:')[-1]
            while doi_str[0] == ' ':
                doi_str = doi_str[1:]
            return doi_str
        elif 'http' in citation.split('. ')[-1]:
            return citation.split('. ')[-1]
        else:
            return None

# ======================================================================================================================

class GetEnteredTextStandAloneImpl:
    """ If user display_input, drop filesPath then return files, exit then return None """
    # -- variables --
    __display_input_text = '> '
    __display_output_text = '>> Read: '

    def read(self):
        entered_str = input(self.__display_input_text)
        if self.__decision_exit(entered_str):
            # if user display_inputs exit meaning then exit
            return None
        else:
            print('{0}{1}'.format(self.__display_output_text, entered_str))
            return entered_str

    def __decision_exit(self, text):
        # -- constants --
        EXIT_TEXTS = ['e', '-e', 'exit', 'exit()', 'Exit', 'Exit()']
        # decision match strings argument and EXIT_TEXTS
        for exit_text in EXIT_TEXTS:
            if text == exit_text:
                return True
        return False

# ======================================================================================================================


if __name__ == '__main__':
    print('-STAND ALONE MODE- apa.py')
    print('Display the article info for your entered citation.')
    getter = APA()
    reader = GetEnteredTextStandAloneImpl()
    # citation = 'Fleshler, M., & Hoffman, H. S. (1962). A progression for generating variable-interval schedules. Journal of the experimental analysis of behavior, 5(4), 529.'
    # article_info = getter.get_all(citation=citation)
    # article_info.print()
    while True:
        print()
        print('Enter the APA format citation...')
        text = reader.read()
        if text is None:
            # exit
            break
        else:
            article_info = getter.get_all(citation=text)
            article_info.print()
