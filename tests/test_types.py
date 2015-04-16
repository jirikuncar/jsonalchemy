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

"""Test types."""

from __future__ import absolute_import

import json

import pytest

from datetime import datetime

from jsonalchemy import factory, types
from jsonalchemy.wrappers import JSONBase, Wrapper as OrigWrapper

from jsonschema import SchemaError, ValidationError

from helpers import abs_path


def test_datetime():
    current_datetime = datetime.now()

    class RecordMeta(JSONBase):
        class Meta:
            creation_date = types.DateTime()

    class Record(RecordMeta()):
        def __init__(self, value=None):
            super(Record, self).__init__(value or {})

    record = Record({})
    record.creation_date = current_datetime

    assert isinstance(record.creation_date, datetime)
    assert record.creation_date == current_datetime

    data = json.dumps(record)
    assert data['creation_date'] == current_datetime.isoformat()


def test_datetime_from_schema():
    current_datetime = datetime.now()

    class RecordMeta(JSONBase):
        class Meta:
            __schema_url__ = abs_path('schemas/creation_date.json')

        def __call__(self, value=None):
            super(RecordMeta, self).__call__(value or {})

    Record = RecordMeta()

    record = Record()
    record.creation_date = current_datetime

    assert isinstance(record.creation_date, datetime)
    assert record.creation_date == current_datetime

    data = json.dumps(record)
    assert data['creation_date'] == current_datetime.isoformat()


def test_properties():

    class RecordMeta(JSONBase):

        class Meta:
            """Schema must contain all properties that should be dumped."""
            __schema__ = factory.compose(
                abs_path('schemas/mixin/keywords.json'),
                abs_path('schemas/mixin/authors.json'),
            )

            class Wrapper(OrigWrapper):

                @property
                def authors(self):
                    return [self.author] + list(self.other_authors)

                @authors.setter
                def authors(self, value):
                    self.author = value[0]
                    self.other_authors = value[1:]

                @property
                def first_keyword(self):
                    return self.keywords[0]

                @property
                def other_keywords(self):
                    return self.keywords[1:]

    Record = RecordMeta()

    record = Record({})
    record.keywords = ['first', 'second', 'other']

    assert record.first_keyword == 'first'
    assert record.other_keywords == ['second', 'other']

    record.author = 'Ellis, J'
    record.other_authors = ['Higgs, P', 'Englert, F']

    assert len(record.authors) == 3

    record.authors = ['First, G', 'Higgs, P', 'Other, G']

    assert record.author == 'First, G'
    assert record.other_authors[1] == 'Other, G'

    record.authors = ['Ellis, J', 'Higgs, P', 'Englert, F']

    assert record.author == 'Ellis, J'
    assert record.other_authors == ['Higgs, P', 'Englert, F']

    with pytest.raises(AttributeError) as excinfo:
        record.first_keyword = 'foo'
    assert "can't set attribute" in str(excinfo.value)

    # FIXME invoke ValidationError
    # with pytest.raises(ValidationError) as excinfo:
    #     record.authors = 3
    # assert "list" in str(excinfo.value)

    data = json.dumps(record.data)

    assert data['first_keyword'] == 'first'
    assert data['other_keywords'] == ['second', 'other']
    assert len(data['authors']) == 3
    assert data['author'] == 'Ellis, J'
    assert data['other_authors'] == ['Higgs, P', 'Englert, F']
