# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Unit test checking behaviour of ``set_default_value``."""

from unittest import TestCase

from jsonalchemy.parser import ModelParser
from jsonalchemy.reader import translate
from jsonalchemy.registry import MetaData
from jsonalchemy.wrappers import SmartJson


class TestOldValue(TestCase):

    """Tests for ``to_int`` function."""

    def setUp(self):
        """Prepare the JSONAlchemy input."""
        self.metadata = MetaData(['jsonalchemy.jsonext', 'testext'])
        self.model_parser = ModelParser(self.metadata)
        self.field_parser = self.model_parser.field_parser
        self.field_definitions = self.field_parser.field_definitions()

    def test_jsonalchemy_tooldvalue(self):
        """Test behaviour of ``set_default_value``.

        In this example, the value provided to the reader in ``d`` subfield
        is in wrong format. However, the behaviour of ``JSONAlchemy`` in such
        case is to skip the value.

        Given the below value of the subfield, the module crashes in
        ``set_default_value``. The error has been caught.
        What is the reason behind the mentioned behaviour needs further
        investigation.
        """

        # Check if it works when the value is provided.
        xml = '''<collection><record><datafield tag="100" ind1=" " ind2=" ">
              <subfield code="a">Guy, Bobby</subfield>
              <subfield code="d">I like trains</subfield>
              <subfield code="g">ACTIVE</subfield>
              <subfield code="q">Bobby Guy</subfield>
              </datafield></record></collection>'''

        simple_record = translate(xml, SmartJson, master_format='marc',
                                  model="test_oldvalue",
                                  metadata=self.metadata)
        self.assertEqual(simple_record['dates']['birth'], None)
