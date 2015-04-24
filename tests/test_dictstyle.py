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

from __future__ import absolute_import

import json
import pytest

from datetime import datetime

from jsonalchemy.dictstyle import JSONDict, JSONList
from jsonalchemy.utils import load_schema_from_url


from jsonschema import SchemaError, ValidationError

from helpers import abs_path


def test_none_in_constructor():
    assert JSONDict() == {}
    assert JSONDict({}) == {}
    assert JSONDict(None, {}) == {}


def test_model_factory():
    """Expected API for end user to generate model from a schema."""
    schema = load_schema_from_url(abs_path('schemas/simple.json'))
    valid_data = {'my_field': 'test'}
    invalid_type_data = {'my_field': 1}
    wrong_field_data = {'wrong_field': 'test'}

    data = JSONDict(valid_data, schema)

    assert 'my_field' in data
    assert set(data.keys()) == set(['my_field'])
    assert data['my_field'] == valid_data['my_field']

    with pytest.raises(ValidationError):
        JSONDict(invalid_type_data, schema=schema)

    with pytest.raises(ValidationError):
        JSONDict(wrong_field_data, schema=schema)

def test_data_setter():
    schema = load_schema_from_url(abs_path('schemas/simple.json'))

    empty_data = JSONDict(schema=schema)
    empty_data['my_field'] = 'valid value'
    assert empty_data['my_field'] == 'valid value'

    with pytest.raises(ValidationError):
        empty_data['my_field'] = 666
    assert empty_data['my_field'] != 666

def test_pop_data():
    schema = load_schema_from_url(abs_path('schemas/required_field.json'))

    data = JSONDict({
        'identifier': 1,
        'my_field': 'test'
    }, schema=schema)

    with pytest.raises(ValidationError):
        del data['identifier']
    assert 'identifier' in data

    del data['my_field']
    assert 'my_field' not in data

def test_set_rollback():
    schema = load_schema_from_url(abs_path('schemas/required_field.json'))

    data = JSONDict({
        'identifier': 1,
    }, schema=schema)

    with pytest.raises(ValidationError):
        data['my_field'] = 666
    assert 'my_field' not in data


def test_list_data():
    schema = load_schema_from_url(abs_path('schemas/list.json'))

    data = JSONList(['foo', 'bar'], schema=schema)

    assert data[0] == 'foo'
    assert len(data) == 2
    assert data == ['foo', 'bar']

    list_data = list(data)
    assert len(list_data) == 2

def test_complex_type_wrapping():
    schema = load_schema_from_url(abs_path('schemas/complex.json'))

    data = JSONDict({
        'authors': [{'family_name': 'Ellis'}]
    }, schema=schema)

    assert data['authors'][0]['family_name'] == 'Ellis'
    assert isinstance(data['authors'], JSONList)

def test_subclassing():
    schema = load_schema_from_url(abs_path('schemas/complex.json'))

    class Record(JSONDict):
        pass

    data = Record({
        'authors': [{'family_name': 'Ellis'}]
    }, schema=schema)

    assert data['authors'][0]['family_name'] == 'Ellis'
    assert isinstance(data['authors'], JSONList)


def test_setting_callbacks():
    schema = load_schema_from_url(abs_path('schemas/complex.json'))
    fixture_data = {
        'authors': [
            {'family_name': 'Ellis'},
            {'family_name': 'Higgs'},
            {'family_name': 'guy'},
        ],
    }
    fixture_callbacks = {
        'authors': {
            None: {
                'family_name': lambda x: x.upper()
            }
        }
    }

    class Record(JSONDict):

        __callbacks__ = fixture_callbacks

    fixtures = [
        JSONDict(fixture_data, schema=schema, callbacks=fixture_callbacks),
        Record(fixture_data, schema=schema),
    ]

    for data in fixtures:
        assert 'authors' in data.callbacks
        assert None in data['authors'].callbacks
        assert all('family_name' in author.callbacks and
                   callable(author.callbacks['family_name'])
                   for author in data['authors'])
        assert data['authors'][0]['family_name'] == 'ELLIS'
        assert data['authors'][-1]['family_name'] == 'GUY'


def _test_subclassing():

    class Record(JSONDict):

        __key_wrappers__ = {
            'authors': Authors,
        }

        @calculated(Authors)
        def authors(self):
            return [self['author']] + self['additional_authors']

    class Authors(JSONList):

        __item_wrappers__ = Author

    class Author(JSONDict):

        @property
        def age(self):
            return datetime.now() - self['birthday']

        wrapper = getattr(self, '__key_wrappers__', {}).get(name, None)
        if wrapper is not None:
            value = wrapper(value)


def _test_attaching():

    def attach(cls, path, callback):

        callbacks = getattr(cls, '__callbacks__', {})
        if len(path) == 1:
            callbacks[path[0]] = callback

    @attach(Record, ['authors'])
    def authors(self):
        return [self['author']] + self['additional_authors']

    @attach(Record, ['authors', None, 'age'])
    def age(self):
        return datetime.now() - self['birthday']

    attach(Record, ['authors'], authors)


    record['authors'][0]['age']
