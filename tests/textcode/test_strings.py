#
# Copyright (c) 2016 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import io
import json
import os

from commoncode.system import py2
from commoncode.system import py3
from commoncode.testcase import FileBasedTesting
from textcode import strings


class TestStrings(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def check_file_strings(self, test_file, expected_file, regen=False):
        test_file = self.get_test_loc(test_file)
        results = list(strings.strings_from_file(test_file))
        expected = self.get_test_loc(expected_file)
        if regen:
            if py2:
                mode = 'wb'
            if py3:
                mode = 'w'
            with io.open(expected, mode) as o:
                o.write(json.dumps(results, indent=2))

        with io.open(expected) as i:
            expected = json.loads(i.read())
        assert expected == results
        return results

    def test_clean_string(self):
        assert list(strings.clean_string('aw w we ww '))
        assert not list(strings.clean_string('ab'))
        assert list(strings.clean_string('abc', min_len=3))
        assert not list(strings.clean_string('abc', min_len=4))
        assert not list(strings.clean_string('abc'))
        assert list(strings.clean_string('aaa\nqqqxy\nbbb'))
        assert list(strings.clean_string('aaa\nqqq\nbbb'))
        assert not list(strings.clean_string('aaaa'))
        assert list(strings.clean_string('abababa'))
        assert not list(strings.clean_string('  tt\nf   '))
        assert list(strings.clean_string('  tt\nfb   '))

    def test_strings_in_file(self):
        expected = [
            u'__text',
            u'__TEXT',
            u'__cstring',
            u'__TEXT',
            u'__jump_table',
            u'__IMPORT',
            u'__textcoal_nt',
            u'__TEXT',
            u'_main',
            u'___i686.get_pc_thunk.bx',
            u'_setlocale',
            u'_yyparse',
            u'/sw/src/fink.build/bison-2.3-1002/bison-2.3/lib/',
            u'main.c',
            u'gcc2_compiled.',
            u':t(0,1)=(0,1)',
            u'main:F(0,2)',
            u'int:t(0,2)=r(0,2);-2147483648;2147483647;'
        ]

        test_file = self.get_test_loc('strings/basic/main.o')
        result = list(strings.strings_from_file(test_file))
        assert expected == result

    def test_strings_in_file_with_min_len(self):
        expected = [
            u'__cstring',
            u'__jump_table',
            u'__IMPORT',
            u'__textcoal_nt',
            u'___i686.get_pc_thunk.bx',
            u'_setlocale',
            u'_yyparse',
            u'/sw/src/fink.build/bison-2.3-1002/bison-2.3/lib/',
            u'gcc2_compiled.',
            u'main:F(0,2)',
            u'int:t(0,2)=r(0,2);-2147483648;2147483647;'
        ]

        test_file = self.get_test_loc('strings/basic/main.o')
        result = list(strings.strings_from_file(test_file, min_len=6))
        assert expected == result


    def test_strings_in_file_does_fail_if_contains_ERROR_string(self):
        test_file = self.get_test_loc('strings/bin/file_stripped')
        list(strings.strings_from_file(test_file))

    def test_file_strings_is_good(self):
        expected = [
            u'__text',
            u'__TEXT',
            u'__cstring',
            u'__TEXT',
            u'__jump_table',
            u'__IMPORT',
            u'__textcoal_nt',
            u'__TEXT',
            u'_main',
            u'___i686.get_pc_thunk.bx',
            u'_setlocale',
            u'_yyparse',
            u'/sw/src/fink.build/bison-2.3-1002/bison-2.3/lib/',
            u'main.c',
            u'gcc2_compiled.',
            u':t(0,1)=(0,1)',
            u'main:F(0,2)',
            u'int:t(0,2)=r(0,2);-2147483648;2147483647;'
        ]

        test_file = self.get_test_loc('strings/basic/main.o')
        result = list(strings.strings_from_file(test_file))
        assert expected == result

    def test_strings_in_fonts(self):
        test_file = 'strings/font/DarkGardenMK.ttf'
        expected_file = 'strings/font/DarkGardenMK.ttf.results'
        self.check_file_strings(test_file, expected_file)

    def test_strings_in_elf(self):
        test_file = self.get_test_loc('strings/elf/shash.i686')
        expected_file = self.get_test_loc('strings/elf/shash.i686.results')
        self.check_file_strings(test_file, expected_file)

    def test_strings_in_obj(self):
        test_file = self.get_test_loc('strings/obj/test.o')
        expected_file = self.get_test_loc('strings/obj/test.o.results')
        self.check_file_strings(test_file, expected_file)

    def test_strings_in_windows_pdb(self):
        test_file = self.get_test_loc('strings/pdb/QTMovieWin.pdb')
        expected_file = self.get_test_loc('strings/pdb/QTMovieWin.pdb.results')
        self.check_file_strings(test_file, expected_file)

    def test_strings_with_unicode_in_windows_pe_are_extracted_correctly(self):
        test_file = self.get_test_loc('strings/pe/7-zip-pe-with-unicode.dll')
        expected_file = self.get_test_loc('strings/pe/7-zip-pe-with-unicode.dll.results')
        result = self.check_file_strings(test_file, expected_file)

        # ascii
        assert any('publicKeyToken="6595b64144ccf1df"' in r for r in result)
        # wide, utf-16-le string
        assert  any('Copyright (c) 1999-2014 Igor Pavlov' in r for r in result)

    def test_strings_in_all_bin(self):
        test_dir = self.get_test_loc('strings/bin', copy=True)
        expec_dir = self.get_test_loc('strings/bin-expected')
        for tf in os.listdir(test_dir):
            test_file = os.path.join(test_dir, tf)
            expected_file = os.path.join(expec_dir, tf + '.strings')
            self.check_file_strings(test_file, expected_file)
