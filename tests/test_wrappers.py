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

"""Test wrappers."""

from __future__ import absolute_import

import pytest

from jsonalchemy.wrappers import (
    JSONBase, Boolean, List, String, Object, Integer, Field
)

from helpers import abs_path


def test_forbiden_type_override():
    with pytest.raises(RuntimeError) as excinfo:
        class AlreadyRegisteredObject(JSONBase):
            schema_type = 'object'


def test_simple_string_wrapper():
    """Test simple wrapping of String."""
    author = Field(String)
    ellis = author("Ellis, J")

    assert ellis == 'Ellis, J'

    clone_ellis = author(ellis)

    assert clone_ellis == ellis


def test_simple_list_wrapper():
    """Test simple wrapping of String."""
    authors = Field(List, items=[String])
    nobles = authors(["Ellis, J", "Higgs, P"])

    assert len(nobles) == 2

    tuple_nobles = authors(("Ellis, J", "Higgs, P"))
    assert len(tuple_nobles) == 2

    with pytest.raises(TypeError) as excinfo:
        authors("Ellis, J")

    assert "is not type of" in str(excinfo.value)

def test_mixed_list_wrapper():
    """Test simple wrapping of String."""
    authors = Field(List)  # any type
    mixed_nobels = authors(["Ellis, J", "Higgs, P", 42, {"this": "that"}])

    assert len(mixed_nobels) == 4

    mix_tuple_nobles = authors(("Ellis, J", "Higgs, P", 42, {"this": "that"}))
    assert len(mix_tuple_nobles) == 4

    with pytest.raises(TypeError) as excinfo:
        authors("Ellis, J")

    assert "is not type of" in str(excinfo.value)

def test_simple_integer_wrapper():
    """Test simple wrapping of String."""
    identifier = Field(Integer)
    my_id = identifier(1)

    assert my_id > 0
    assert my_id < 2
    assert my_id <= 1
    assert my_id >= 1
    assert my_id == 1
    assert my_id != 0

    with pytest.raises(TypeError) as excinfo:
        identifier("1")

    assert "is not type of" in str(excinfo.value)


def test_simple_bool_wrapper():
    """Test simple wrapping of Boolean."""
    flag = Field(Boolean)
    my_flag = flag(True)
    assert my_flag

    my_flag_is_down = flag(False)
    assert not my_flag_is_down

    with pytest.raises(TypeError) as excinfo:
        flag("True")

    with pytest.raises(TypeError) as excinfo:
        flag(1)


def test_simple_object_wrapper():
    """Test simple wrapping of String."""
    author = Field(Object)
    ellis = author({
        "full_name": "Ellis, John R."
    })

    assert ellis == {
        "full_name": "Ellis, John R."
    }

    with pytest.raises(TypeError) as excinfo:
        author("Ellis, John R.")

    assert "is not type of" in str(excinfo.value)


def test_wrapper_composability():

    class Record(Object):
        identifier = Field(Integer)
        title = Field(String)
        keywords = Field(List)

    record = Record({
        'identifier': 1,
        'title': 'Test',
        'keywords': ['foo', 'bar'],
    })

    assert record.identifier == 1
    assert record.title == 'Test'
    assert record.keywords == ['foo', 'bar']

    with pytest.raises(AttributeError) as excinfo:
        getattr(record, 'not_existent_attribute')

    with pytest.raises(Exception) as excinfo:
        record = Record({
            'not_in_schema': 'Any Value',
        })


def test_wrapper_recursive_composability():

    class Record(Object):
        identifier = Field(Integer)
        title = Field(String)
        keywords = Field(List)

        class Author(Object):
            full_name = Field(String)

        author = Field(Author)

    record = Record({
        'identifier': 1,
        'title': 'Test',
        'keywords': ['foo', 'bar'],
        'author': {'full_name': 'Ellis, J'}
    })

    assert record.identifier == 1
    assert record.title == 'Test'
    assert record.keywords == ['foo', 'bar']
    assert record.author.full_name == 'Ellis, J'

    with pytest.raises(AttributeError) as excinfo:
        getattr(record.author, 'not_existent_attribute')

    with pytest.raises(Exception) as excinfo:
        record = Record({
            'author': {'not_in_schema': 'Any Value'},
        })


def test_wrapper_composability():

    class Record(Object):
        identifier = Field(Integer)
        title = Field(String)
        keywords = Field(List)

        class Author(Object):
            full_name = Field(String)

        authors = Field(List, items=[Author])

    record = Record({
        'identifier': 1,
        'title': 'Test',
        'keywords': ['foo', 'bar'],
        'authors': [
            {'full_name': 'Ellis, J'},
            {'full_name': 'Higgs, P'},
            {'full_name': 'Englert, F'},
        ]
    })

    assert record.identifier == 1
    assert record.title == 'Test'
    assert record.keywords == ['foo', 'bar']
    assert len(record.authors) == 3
    assert record.authors[0].full_name == 'Ellis, J'
    assert record.authors[2].full_name == 'Englert, F'

    with pytest.raises(IndexError) as excinfo:
        record.authors[3]

    del record.authors[1]
    assert len(record.authors) == 2
    assert record.authors[1].full_name == 'Englert, F'

    with pytest.raises(AttributeError) as excinfo:
        getattr(record.authors[0], 'not_existent_attribute')

    with pytest.raises(TypeError) as excinfo:
        record.authors.append('Ellis, J')

    # TODO splice


def test_tricky_keys():

    class Data(Object):
        schema = Field(String)
        data = Field(String)

    data = Data({'data': 'data', 'schema': 'schema'})

    assert data['data'] == 'data'
    assert data['schema'] == 'schema'

    assert data.data['data'] == 'data'
    assert data.data['schema'] == 'schema'

    data = Data({})
    data['data'] = 'foo'
    data['schema'] = 'bar'

    assert data['data'] == 'foo'
    assert data['schema'] == 'bar'


def test_schema_and_schema_url():
    with pytest.raises(RuntimeError) as excinfo:
        class TooManySchema(String):
            __schema__ = { 'type': 'string' }
            __schema_url__ = abs_path('schemas/compose/title.json')
