# -*- coding: utf-8 -*-
#
# This file is part of JSONAlchemy.
# Copyright (C) 2015 CERN.
#
# JSONAlchemy is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# JSONAlchemy is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JSONAlchemy; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Unit tests for testing Jsonext's functions."""

import sys

from os.path import dirname, realpath
from unittest import TestCase

from jsonalchemy.jsonext.functions.to_int import to_int
from jsonalchemy.parser import ModelParser
from jsonalchemy.reader import translate, split_blob
from jsonalchemy.registry import MetaData
from jsonalchemy.wrappers import SmartJson

sys.path.append(dirname(realpath(__file__)))


class TestFunctions(TestCase):

    def setUp(self):
        self.metadata = MetaData([
            'jsonalchemy.jsonext',
            'testext',
        ])
        self.model_parser = ModelParser(self.metadata)
        self.field_parser = self.model_parser.field_parser

    def test_toint_results(self):
        """Test ``to_int`` function itself."""
        assert to_int(None) is None
        assert to_int("-1") == -1

    def test_jsonalchemy_toint_usage(self):
        """Test the usage of ``to_int`` function in real life example.

        The ``test_toint`` model contains a field which contains an integer
        subfield. Whenever the record is obtained from ``MARCXML``, the
        string in mentioned subfield has to be converted to an integer.

        However, JSONAlchemy fills every absent subfield with a ``None`` value.
        If the record is not provided with the integer subfield and the
        built-in ``int`` function is used, the code will crash.

        The ``to_int`` function used inside definition of ``test_toint`` field
        prevents it. Here the unprovided subfield is ``999__a``.
        """
        xml = '<collection><record><datafield tag="999" ind1="" ind2= "">' \
              '<subfield code="b">Value</subfield></datafield></record>' \
              '</collection>'
        simple_record = translate(xml, SmartJson, master_format='marc',
                                  model="test_toint", metadata=self.metadata)
        assert len(simple_record.__dict__['_dict']['__meta_metadata__'][
            '__errors__']) == 0

        # Check if it works when the value is provided.
        xml = '<collection><record><datafield tag="999" ind1="" ind2= "">' \
              '<subfield code="a">9999</subfield>' \
              '<subfield code="b">Value</subfield></datafield></record>' \
              '</collection>'

        simple_record = translate(xml, SmartJson, master_format='marc',
                                  model="test_toint", metadata=self.metadata)
        self.assertEqual(simple_record['with_integers'][0]['some_int'], 9999)
