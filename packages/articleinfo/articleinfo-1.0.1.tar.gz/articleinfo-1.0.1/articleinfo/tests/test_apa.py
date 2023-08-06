#!/usr/bin/python
# -*- coding: utf-8 -*-

# === About ============================================================================================================

"""
 test_apa.py

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
import unittest
""" Third party library """
""" Local library """
from articleinfo.getArticleInfoFromCitation.apa import APA

# === CONSTANTS ========================================================================================================

# === User Parameters ==================================================================================================

# === variables ========================================================================================================

# ======================================================================================================================


class TestAPA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('class TestAPA(unittest.TestCase):')
        print('def setUpClass(cls):')

    @classmethod
    def tearDownClass(cls):
        print('def tearDownClass(cls):')

    def setUp(self):
        print('def setUp(self):')
        self.getter = APA()

    def tearDown(self):
        print('def tearDown(self):')

    def test_APA_citation_SingleAuthor_InSubtitle_NoIssue(self):
        print('def test_APA_citation_SingleAuthor_InSubtitle_NoIssue(self):')
        citation = 'Schooler, D. (2008). Real women have curves: A longitudinal investigation of TV and the body image development of Latina adolescents. Journal of Adolescent Research, 23, 132-153. doi:10.1177/0743558407310712'
        article_info = self.getter.get_all(citation=citation)
        self.assertEqual(article_info.first_author, 'Schooler, D.')
        self.assertEqual(article_info.authors, ['Schooler, D.'])
        self.assertEqual(article_info.year, '2008')
        self.assertEqual(article_info.article_title, 'Real women have curves: A longitudinal investigation of TV and the body image development of Latina adolescents.')
        self.assertEqual(article_info.article_main_title, 'Real women have curves.')
        self.assertEqual(article_info.article_sub_title, 'A longitudinal investigation of TV and the body image development of Latina adolescents.')
        self.assertEqual(article_info.journal_title, 'Journal of Adolescent Research')
        self.assertEqual(article_info.volume, '23')
        self.assertEqual(article_info.issue, '')
        self.assertEqual(article_info.pages, ['132', '153'])
        self.assertEqual(article_info.doi, '10.1177/0743558407310712')

    def test_APA_citation_TooManyAuthors_InIssue_NoDOI(self):
        print('def test_APA_citation_TooManyAuthors_InIssue_NoDOI(self):')
        citation = 'Howe, K., Clark, M. D., Torroja, C. F., Torrance, J., Berthelot, C., Muffato, M., ... & McLaren, S. (2013). The zebrafish reference genome sequence and its relationship to the human genome. Nature, 496(7446), 498-503.'
        article_info = self.getter.get_all(citation=citation)
        self.assertEqual(article_info.first_author, 'Howe, K.')
        self.assertEqual(article_info.authors, ['Howe, K.', 'Clark, M. D.', 'Torroja, C. F.', 'Torrance, J.', 'Berthelot, C.', 'Muffato, M.', 'McLaren, S.'])
        self.assertEqual(article_info.year, '2013')
        self.assertEqual(article_info.article_title, 'The zebrafish reference genome sequence and its relationship to the human genome.')
        self.assertEqual(article_info.article_main_title, 'The zebrafish reference genome sequence and its relationship to the human genome.')
        self.assertEqual(article_info.article_sub_title, '')
        self.assertEqual(article_info.journal_title, 'Nature')
        self.assertEqual(article_info.volume, '496')
        self.assertEqual(article_info.issue, '7446')
        self.assertEqual(article_info.pages, ['498', '503'])
        self.assertEqual(article_info.doi, '')

    def test_APA_citation_TwoAuthors_SinglePage_NoDOI(self):
        print('def test_APA_citation_TwoAuthors_SinglePage_NoDOI(self):')
        citation = 'Fleshler, M., & Hoffman, H. S. (1962). A progression for generating variable-interval schedules. Journal of the experimental analysis of behavior, 5(4), 529.'
        article_info = self.getter.get_all(citation=citation)
        self.assertEqual(article_info.first_author, 'Fleshler, M.')
        self.assertEqual(article_info.authors, ['Fleshler, M.', 'Hoffman, H. S.'])
        self.assertEqual(article_info.year, '1962')
        self.assertEqual(article_info.article_title, 'A progression for generating variable-interval schedules.')
        self.assertEqual(article_info.article_main_title, 'A progression for generating variable-interval schedules.')
        self.assertEqual(article_info.article_sub_title, '')
        self.assertEqual(article_info.journal_title, 'Journal of the experimental analysis of behavior')
        self.assertEqual(article_info.volume, '5')
        self.assertEqual(article_info.issue, '4')
        self.assertEqual(article_info.pages, ['529'])
        self.assertEqual(article_info.doi, '')

    def test_APA_citation_ThreeAuthors_CommaInSubTitle_NoDOI(self):
        print('def test_APA_citation_ThreeAuthors_CommaInSubTitle_NoDOI(self):')
        citation = 'Bouton, M. E., Winterbauer, N. E., & Todd, T. P. (2012). Relapse processes after the extinction of instrumental learning: renewal, resurgence, and reacquisition. Behavioural processes, 90(1), 130-141.'
        article_info = self.getter.get_all(citation=citation)
        self.assertEqual(article_info.first_author, 'Bouton, M. E.')
        self.assertEqual(article_info.authors, ['Bouton, M. E.', 'Winterbauer, N. E.', 'Todd, T. P.'])
        self.assertEqual(article_info.year, '2012')
        self.assertEqual(article_info.article_title, 'Relapse processes after the extinction of instrumental learning: renewal, resurgence, and reacquisition.')
        self.assertEqual(article_info.article_main_title, 'Relapse processes after the extinction of instrumental learning.')
        self.assertEqual(article_info.article_sub_title, 'renewal, resurgence, and reacquisition.')
        self.assertEqual(article_info.journal_title, 'Behavioural processes')
        self.assertEqual(article_info.volume, '90')
        self.assertEqual(article_info.issue, '1')
        self.assertEqual(article_info.pages, ['130', '141'])
        self.assertEqual(article_info.doi, '')

    def test_APA_citation_TwoAuthors_BracketsAndPeriodInTitle_NoDOI(self):
        print('def test_APA_citation_TwoAuthors_BracketsAndPeriodInTitle_NoDOI(self):')
        citation = 'Dielenberg, R. A., & McGregor, I. S. (1999). Habituation of the hiding response to cat odor in rats (Rattus norvegicus). Journal of Comparative Psychology, 113(4), 376.'
        article_info = self.getter.get_all(citation=citation)
        self.assertEqual(article_info.first_author, 'Dielenberg, R. A.')
        self.assertEqual(article_info.authors, ['Dielenberg, R. A.', 'McGregor, I. S.'])
        self.assertEqual(article_info.year, '1999')
        self.assertEqual(article_info.article_title, 'Habituation of the hiding response to cat odor in rats (Rattus norvegicus).')
        self.assertEqual(article_info.article_main_title, 'Habituation of the hiding response to cat odor in rats (Rattus norvegicus).')
        self.assertEqual(article_info.article_sub_title, '')
        self.assertEqual(article_info.journal_title, 'Journal of Comparative Psychology')
        self.assertEqual(article_info.volume, '113')
        self.assertEqual(article_info.issue, '4')
        self.assertEqual(article_info.pages, ['376'])
        self.assertEqual(article_info.doi, '')

    def test_APA_citation_SingleAuthor_UpperCaseInTitle_PeriodInSubTitle_ApostropheInSubTitle_NoDOI(self):
        citation = 'Nevin, J. A. (1969). SIGNAL DETECTION THEORY AND OPERANT BEHAVIOR: A Review of David M. Green and John A. Swets\' Signal Detection Theory and Psychophysics. Journal of the Experimental Analysis of Behavior, 12(3), 475-480.'
        article_info = self.getter.get_all(citation=citation)
        self.assertEqual(article_info.first_author, 'Nevin, J. A.')
        self.assertEqual(article_info.authors, ['Nevin, J. A.'])
        self.assertEqual(article_info.year, '1969')
        self.assertEqual(article_info.article_title, 'SIGNAL DETECTION THEORY AND OPERANT BEHAVIOR: A Review of David M. Green and John A. Swets\' Signal Detection Theory and Psychophysics.')
        self.assertEqual(article_info.article_main_title, 'SIGNAL DETECTION THEORY AND OPERANT BEHAVIOR.')
        self.assertEqual(article_info.article_sub_title, 'A Review of David M. Green and John A. Swets\' Signal Detection Theory and Psychophysics.')
        self.assertEqual(article_info.journal_title, 'Journal of the Experimental Analysis of Behavior')
        self.assertEqual(article_info.volume, '12')
        self.assertEqual(article_info.issue, '3')
        self.assertEqual(article_info.pages, ['475', '480'])
        self.assertEqual(article_info.doi, '')

    def test_APA_citation_FiveAuthors_QuotationMarkInTitle_QuestionMarkInTitle_HyphenInTitle_NoDOI(self):
        citation = 'Magoon, M. A., Critchfield, T. S., Merrill, D., Newland, M. C., & Schneider, W. J. (2017). Are positive and negative reinforcement “different”? Insights from a free‐operant differential outcomes effect. Journal of the experimental analysis of behavior, 107(1), 39-64.'
        article_info = self.getter.get_all(citation=citation)
        self.assertEqual(article_info.first_author, 'Magoon, M. A.')
        self.assertEqual(article_info.authors, ['Magoon, M. A.', 'Critchfield, T. S.', 'Merrill, D.', 'Newland, M. C.', 'Schneider, W. J.'])
        self.assertEqual(article_info.year, '2017')
        self.assertEqual(article_info.article_title, 'Are positive and negative reinforcement “different”? Insights from a free‐operant differential outcomes effect.')
        self.assertEqual(article_info.article_main_title, 'Are positive and negative reinforcement “different”? Insights from a free‐operant differential outcomes effect.')
        self.assertEqual(article_info.article_sub_title, '')
        self.assertEqual(article_info.journal_title, 'Journal of the experimental analysis of behavior')
        self.assertEqual(article_info.volume, '107')
        self.assertEqual(article_info.issue, '1')
        self.assertEqual(article_info.pages, ['39', '64'])
        self.assertEqual(article_info.doi, '')

    def test_APA_citation_SingleAuthor_UpperCaseInTitle_HyphenInTitle_UpperCaseInSubTitle_QuestionMarkInSubTitle_NoDOI(self):
        citation = 'Iversen, I. H. (1997). MATCHING‐TO‐SAMPLE PERFORMANCE IN RATS: A CASE OF MISTAKEN IDENTITY?. Journal of the Experimental Analysis of Behavior, 68(1), 27-45.'
        article_info = self.getter.get_all(citation=citation)
        self.assertEqual(article_info.first_author, 'Iversen, I. H.')
        self.assertEqual(article_info.authors, ['Iversen, I. H.'])
        self.assertEqual(article_info.year, '1997')
        self.assertEqual(article_info.article_title, 'MATCHING‐TO‐SAMPLE PERFORMANCE IN RATS: A CASE OF MISTAKEN IDENTITY?.')
        self.assertEqual(article_info.article_main_title, 'MATCHING‐TO‐SAMPLE PERFORMANCE IN RATS.')
        self.assertEqual(article_info.article_sub_title, 'A CASE OF MISTAKEN IDENTITY?.')
        self.assertEqual(article_info.journal_title, 'Journal of the Experimental Analysis of Behavior')
        self.assertEqual(article_info.volume, '68')
        self.assertEqual(article_info.issue, '1')
        self.assertEqual(article_info.pages, ['27', '45'])
        self.assertEqual(article_info.doi, '')


# ======================================================================================================================


if __name__ == '__main__':
    unittest.main()
