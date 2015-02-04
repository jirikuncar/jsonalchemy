# -*- coding: utf-8 -*-
#
# This file is part of JSONAlchemy.
# Copyright (C) 2014, 2015 CERN.
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

"""Unit tests for the storage engine."""

import sys

from os.path import dirname, realpath
from unittest import TestCase

from jsonalchemy.parser import ModelParser
from jsonalchemy.reader import translate, split_blob
from jsonalchemy.registry import MetaData
from jsonalchemy.wrappers import SmartJson
from jsonalchemy.jsonext.engines.memory import MemoryStorage

sys.path.append(dirname(realpath(__file__)))


def class_factory(engine):
    from jsonalchemy.wrappers import SmartJson

    class DummyJson(SmartJson):
        storage_engine = engine
    return DummyJson


class TestStorageEngineConfig(TestCase):
    """Test for configuration of storage engine."""

    def setUp(self):
        self.metadata = MetaData(['jsonalchemy.jsonext', 'testext'])
        self.model_parser = ModelParser(self.metadata)
        self.field_parser = self.model_parser.field_parser

    def test_memory_database(self):
        database = {}
        storage_engine = MemoryStorage(database=database)
        DummyJson = class_factory(storage_engine)
        database[1] = DummyJson({'_id': 1}, master_format='json',
                                metadata=self.metadata)

        self.assertEqual(DummyJson.storage_engine.get_one(1)['_id'],
                         database[1]['_id'])
