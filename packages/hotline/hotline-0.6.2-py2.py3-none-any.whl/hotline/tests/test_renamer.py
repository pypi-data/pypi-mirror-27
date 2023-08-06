# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import unittest
from hotline.renamer import *


class TestRenamer(unittest.TestCase):

    def test_AddPrefixToken(self):
        '''AddPrefixToken'''

        assert AddPrefixToken.match('pre_+')

        bad = ['+_suff', '-rem', 'rem-', 'sub sub']
        for b in bad:
            assert not AddPrefixToken.match(b)

        t = AddPrefixToken('pre_+')
        assert t('funk') == 'pre_funk'

    def test_AddSuffixToken(self):
        '''AddSuffixToken'''

        assert AddSuffixToken.match('+_suff')

        bad = ['pre_+', '-rem', 'rem-', 'sub sub']
        for b in bad:
            assert not AddSuffixToken.match(b)

        t = AddSuffixToken('+_suff')
        assert t('funk') == 'funk_suff'

    def test_RemoveToken(self):
        '''RemoveToken'''

        assert RemoveToken.match('-rem')

        bad = ['pre_+', '+_suff', 'rem-', 'sub sub']
        for b in bad:
            assert not RemoveToken.match(b)

        t = RemoveToken('-rem')
        assert t('remove') == 'ove'

    def test_SubstituteToken(self):
        '''SubstituteToken'''

        assert SubstituteToken.match('a', 'b')

        bad = [('pre_+', 'b'), ('a', '+_suff'), ('-rem', '+pre_+')]
        for b in bad:
            assert not SubstituteToken.match(*b)

        t = SubstituteToken('c', 'b')
        assert t('cat') == 'bat'

    def test_preprocess_string(self):
        '''preprocess_string'''

        data = [
            ('a_##', ('a_{0:0>2}', [1])),
            ('a_##(10)', ('a_{0:0>2}', [10])),
            ('a_##_b_###(20)_c', ('a_{0:0>2}_b_{1:0>3}_c', [1, 20]))
        ]

        for in_str, result in data:
            assert preprocess_string(in_str) == result

    def test_tokenize_string(self):
        # TODO: Test tokenize string
        assert True

    def test_renamer(self):
        # TODO: Test renamer
        assert True
