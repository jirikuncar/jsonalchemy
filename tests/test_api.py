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

import pytest

from datetime import datetime

from jsonalchemy import factory
from jsonalchemy.wrappers import JSONBase, Object, String

from jsonschema import SchemaError, ValidationError

from helpers import abs_path


def test_model_factory():
    """Expected API for end user to generate model from a schema."""
    SimpleRecord = factory.model_factory(abs_path('schemas/simple.json'))

    assert hasattr(SimpleRecord, '__schema__')
    assert hasattr(SimpleRecord, 'my_field')


def test_non_existent_schema():
    """Test that an error is raised should the schema URL be wrong."""
    with pytest.raises(IOError) as excinfo:
        factory.model_factory('/not_existent/schema.json')
    assert 'not_existent/schema.json' in str(excinfo.value)


def test_invalid_schema():
    """Test that an error is raised should the schema be invalid."""
    with pytest.raises(ValueError) as excinfo:
        factory.model_factory(abs_path('schemas/missing_bracket.json'))
    assert 'ValueError' in str(excinfo)

    with pytest.raises(SchemaError) as excinfo:
        factory.model_factory(abs_path('schemas/invalid_json_schema.json'))
    assert 'SchemaError' in str(excinfo)


def test_meta():
    """Internal model structure when schema url is used."""
    class SimpleRecord(JSONBase):
        class Meta:
            __schema_url__ = abs_path('schemas/simple.json')

    assert hasattr(SimpleRecord, '__schema__')
    assert hasattr(SimpleRecord, 'my_field')


def test_schema_dict():
    """Internal model structure when schema dict is used."""
    class SimpleRecord(JSONBase):
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


def test_type_from_schema():
    """Test type from schema."""
    class StringField(JSONBase):
        class Meta:
            __schema__ = {
                'title': 'Test String Field',
                'type': 'string',
            }

    class ProperStringField(String):
        class Meta:
            __schema__ = {
                'title': 'Proper String Field',
                'type': 'string',
            }

    with pytest.raises(TypeError) as excinfo:
        class Mismatched(Object):
            class Meta:
                __schema__ = {
                    'title': 'This is not a string Field',
                    'type': 'string',
                }

    test_string_field = StringField()

    test_value = test_string_field('test value')
    assert test_value == 'test value'

    with pytest.raises(TypeError) as excinfo:
        test_string_field(1)


def test_recursive_type_creation():

    class RecordMeta(Object):

        class Meta:

            __schema__ = {
                'type': 'object',
                'properties': {
                    'identifier': {'type': 'integer'},
                    'title': {'type': 'string'},
                    'keywords': {'type': 'array', 'items': {
                        'type': 'string',
                    }},
                    'author': {
                        'type': 'object',
                        'properties': {
                            'full_name': {'type': 'string'},
                        },
                    },
                },
            }

    Record = RecordMeta()

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


def test_list_field():
    """Test that the schema type resolution are correct and Pythonic."""
    Record = factory.model_factory(abs_path('schemas/record_with_title.json'))

    assert Record.__schema__['type'] == 'object'
    assert Record.authors.__schema__['type'] == 'array'

    record = Record({})

    assert isinstance(record.authors, list)


def test_default_value():
    """Test default value and __eq__ method."""
    class FieldWithDefault(JSONBase):
        class Meta:
            __schema__ = {
                'title': 'Field with default',
                'type': 'string',
                'default': 'foo',
            }

    class FieldWithDefault2(String):

        """Field with default"""

        @classmethod
        def default(cls):
            return 'foo'

    assert hasattr(FieldWithDefault, '__schema__')

    field = FieldWithDefault({})
    assert field == 'foo'

    class ModelWithDefaultField(JSONBase):
        field = FieldWithDefault()

    data = ModelWithDefaultField({})
    assert model.field == 'foo'

    data.field = 'bar'
    assert field == 'foo'
    assert data.field == 'bar'


def test_schema_references():
    """Test reference resolution between schemas."""
    Title = factory.model_factory(abs_path('schemas/title.json'))
    Record = factory.model_factory(abs_path('schemas/record_with_title.json'))

    #assert Record.title.__schema__ == Title.__schema__
    assert type(Record.title) == type(Title)
    assert 'id' in Title.__schema__
    assert Record.title.__schema__['$ref'] == Title.__schema__['id']


def test_model_valid_setting():
    """Test that valid values are properly set in model object."""
    SimpleRecord = factory.model_factory(abs_path('schemas/simple.json'))
    record = SimpleRecord({})

    record.my_field = "This is legal"
    assert record.my_field == "This is legal"

    record.my_field = "æøå"
    assert record.my_field == "æøå"

    record.my_field = u"æøå"
    assert record.my_field == u"æøå"


def test_complex_model_valid_setting():
    """Test that valid values are properly set in model object."""
    ComplexRecord = factory.model_factory(abs_path('schemas/complex.json'))
    record = ComplexRecord({'authors': []})

    record.authors.append({
        "given_name": "Iron",
        "family_name": "Man",
        "affiliation": "Stark Inc."
    })
    assert record.authors == [{
        "given_name": "Iron",
        "family_name": "Man",
        "affiliation": "Stark Inc."
    }]


def test_model_invalid_setting():
    """Test that invalid values raises a ValidationError."""
    SimpleRecord = factory.model_factory(abs_path('schemas/simple.json'))
    record = SimpleRecord({})

    with pytest.raises(TypeError) as excinfo:
        record.my_field = 666


def test_single_inheritance():
    """Field override and single inheritance."""
    BaseRecord = factory.model_factory(abs_path('schemas/inherit/base.json'))
    Record = factory.model_factory(abs_path('schemas/inherit/title.json'),
                                   bases=(BaseRecord, ))

    assert BaseRecord.title.__schema__['type'] == 'string'
    assert Record.title.__schema__['type'] == 'object'

    assert BaseRecord.author == Record.author


def test_simple_composability():
    """Compose simple types to new class."""
    Title = factory.model_factory(abs_path('schemas/compose/title.json'))
    Author = factory.model_factory(abs_path('schemas/compose/author.json'))

    class Record(Object):
        class Meta:
            title = Title
            author = Author

    assert Record.title.__schema__ == Title.__schema__
    assert Record.author.__schema__ == Author.__schema__

    assert len(Record.__schema__['properties']) >= 2


def test_mixins():
    """Compose objects to new class."""
    Title = factory.model_factory(abs_path('schemas/mixin/title.json'))
    Author = factory.model_factory(abs_path('schemas/mixin/author.json'))

    assert Title.__schema__['type'] == 'object'
    assert Author.__schema__['type'] == 'object'

    class Record(JSONBase):
        class Meta:
            __schema__ = factory.compose(
                abs_path('schemas/mixin/title.json'),
                abs_path('schemas/mixin/author.json')
            )

    assert Record.title.__schema__ == Title.title.__schema__
    assert Record.author.__schema__ == Author.author.__schema__

# TODO overlaping fields in mixins
