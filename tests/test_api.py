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

"""Test API."""

import pytest

from datetime import datetime

from jsonalchemy import JSONSchemaBase, factory

from jsonschema import SchemaError


def test_model_factory():
    """Expected API for end user to generate model from a schema."""
    SimpleRecord = factory.model_factory(object, 'schemas/simple.json')

    assert hasattr(SimpleRecord, '__schema__')
    assert hasattr(SimpleRecord, 'my_field')


def test_non_existent_schema():
    with pytest.raises(IOError) as excinfo:
        factory.model_factory(object, 'not_existent/schema.json')
        assert 'not_existent/schema.json' in str(excinfo.value)


def test_invalid_schema():
    with pytest.raises(ValueError) as excinfo:
        factory.model_factory(object, 'schemas/missing_bracket.json')
        assert 'ValueError' in str(excinfo.value)

    with pytest.raises(SchemaError) as excinfo:
        factory.model_factory(object, 'schemas/invalid_json_schema.json')
        assert 'SchemaError' in str(excinfo.value)


def test_meta():
    """Internal model structure when schema url is used."""

    class SimpleRecord(JSONSchemaBase):
        class Meta:
            __schema_url__ = 'schemas/simple.json'

    assert hasattr(SimpleRecord, '__schema__')
    assert hasattr(SimpleRecord, 'my_field')


def test_schema_dict():
    """Internal model structure when schema dict is used."""

    class SimpleRecord(JSONSchemaBase):
        class Meta:
            __schema__ = {
                'title': 'Simple Schema',
                'type': 'object',
                'properties': {
                    'my_field': {'type': 'string'}
                },
            }

    assert hasattr(SimpleRecord, '__schema__')
    assert hasattr(SimpleRecord, 'my_field')


def test_list_field():

    Record = factory.model_factory(object, 'schemas/record_with_title.json')

    assert Record.__schema__['type'] == 'object'
    assert Record.authors.__schema__['type'] == 'array'

    record = Record()

    assert isinstance(record.authors, list)


def test_default_value():
    """Test default value and __eq__ method."""

    class FieldWithDefault(JSONSchemaBase):
        class Meta:
            __schema__ = {
                'title': 'Field with default',
                'type': 'string',
                'default': 'foo',
            }

    assert hasattr(FieldWithDefault, '__schema__')

    field = FieldWithDefault()
    assert field == 'foo'


def test_schema_references():

    Title = factory.model_factory(object, 'schemas/title.json')

    Record = factory.model_factory(object, 'schemas/record_with_title.json')

    #assert Record.title.__schema__ == Title.__schema__
    assert type(Record.title) == type(Title)
    assert 'id' in Title.__schema__
    assert Record.title.__schema__['$ref'] == Title.__schema__['id']
