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

"""Unit tests for the JSONAlchemy bases."""

import sys

from datetime import datetime
from os.path import dirname, realpath
from testext import functions
from unittest import TestCase

from jsonalchemy.parser import (
    ModelParser, guess_legacy_field_names, get_producer_rules
)
from jsonalchemy.reader import translate
from jsonalchemy.registry import MetaData
from jsonalchemy.wrappers import SmartJson

sys.path.append(dirname(realpath(__file__)))


class TestVersionable(TestCase):

    def setUp(self):
        self.metadata = MetaData(['jsonalchemy.jsonext', 'testext'])
        self.model_parser = ModelParser(self.metadata)
        self.field_parser = self.model_parser.field_parser

    def test_versionable_base(self):
        """Versionable - model creation"""
        from jsonalchemy.jsonext.engines import memory
        storage = {}

        class _VersionableJson(SmartJson):

            storage_engine = memory.MemoryStorage(database=storage)

            @classmethod
            def create(cls, data, model='test_versionable',
                       master_format='json', **kwargs):
                document = translate(
                    data, cls, master_format=master_format,
                    model=model, metadata=self.metadata, **kwargs)
                cls.storage_engine.save_one(document.dumps())
                document.bind(self.metadata)
                return document

            @classmethod
            def get_one(cls, _id):
                return cls(cls.storage_engine.get_one(_id),
                           metadata=self.metadata)

            def _save(self):
                try:
                    return self.__class__.storage_engine.update_one(
                        self.dumps(), id=self['_id'])
                except:
                    return self.__class__.storage_engine.save_one(
                        self.dumps(), id=self['_id'])

            def update(self):
                self['modification_date'] = datetime.now()
                return self._save()

        v0 = _VersionableJson.create({'title': 'Version 0'})
        self.assertTrue('title' in v0)
        self.assertTrue('Version 0' in v0['title'])

        v0['title'] = 'Version 1'
        v1 = v0.update()

        v_older = _VersionableJson.get_one(v1['older_version'])

        self.assertTrue('older_version' in v1)
        self.assertTrue(v_older['_id'] in v1['older_version'])
        self.assertTrue('Version 1' in v1['title'])
        self.assertTrue(v1['_id'] in v_older['newer_version'])


class TestHidden(TestCase):

    def setUp(self):
        self.metadata = MetaData(['jsonalchemy.jsonext', 'testext'])
        self.model_parser = ModelParser(self.metadata)
        self.field_parser = self.model_parser.field_parser

    def test_dumps_hidden(self):
        data = {'title': 'Test Title'}

        document = translate(
            data, SmartJson, master_format='json',
            model='test_hidden', metadata=self.metadata)

        json = document.dumps()
        self.assertTrue('title' in json)
        self.assertTrue('hidden_basic' in json)

        json = document.dumps(filter_hidden=True)
        self.assertTrue('title' in json)
        self.assertFalse('hidden_basic' in json)
