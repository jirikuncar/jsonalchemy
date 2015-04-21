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
# JSONAlchemy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JSONAlchemy; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Wrappers."""

from collections import namedtuple
from jsonschema import SchemaError
from six import iteritems, add_metaclass

from .utils import load_schema_from_url


class Field(object):

    def __init__(self, field_type, *args, **kwargs):
        self.field_type = field_type
        self.args = args
        self.kwargs = kwargs

    def __call__(self, document):
        return self.field_type(document, *self.args, **self.kwargs)


class MetaSchema(type):

    __schema_registry__ = {}

    def __new__(cls, name, bases, attrs):
        schema_url = attrs.get('__schema_url__', None)
        if schema_url:
            schema = load_schema_from_url(schema_url)
            if '__schema__' in attrs:
                raise RuntimeError()
        else:
            schema = attrs.get('__schema__', {})

        # Store modification back in attributes.
        attrs['__schema__'] = schema

        # TODO cls.__doc__ to title if not there
        schema_type = schema.get('type', None)
        if schema_type:
            attrs = cls.__schema_registry__[schema_type].from_schema(attrs)

        for base in bases:
            if hasattr(base, 'from_schema'):
                attrs = base.from_schema(attrs)

        # Check compatibility of JSON Schema type with my base classes.
        if schema_type and not any(
                issubclass(cls.__schema_registry__[schema_type], base)
                for base in bases):
            raise TypeError(
                'Type specified in the schema ("{0}") is not a subclass '
                'of any of {1}'.format(schema_type, bases))

        if schema_type and not any(
                issubclass(base, cls.__schema_registry__[schema_type])
                for base in bases):
            bases = (cls.__schema_registry__[schema_type], ) + bases

        schema_class = super(MetaSchema, cls).__new__(cls, name, bases, attrs)
        schema_type = attrs.get('schema_type', None)
        if schema_type in cls.__schema_registry__:
            raise RuntimeError('"{0}" has been already registered.'.format(
                schema_type
            ))
        elif schema_type:
            cls.__schema_registry__[schema_type] = schema_class

        return schema_class

    @property
    def __schema__(cls):
        return {'type': cls.schema_type}


def create_type_from_schema(schema, bases=()):
    schema_type = schema['type']
    schema_base = MetaSchema.__schema_registry__[schema_type]

    return type(schema_base.__name__, bases + (schema_base, ), {
        'Meta': type('Meta', (object, ), {
            '__schema__': schema
        }),
    })


def schema_to_type(schema):
    schema_type = schema.get('type', None)
    try:
        return create_type_from_schema(schema)()
    except KeyError:
        raise SchemaError('"{0}" is not a valid schema'.format(schema_type))


@add_metaclass(MetaSchema)
class JSONBase(object):

    def __init__(self, value):
        if not (isinstance(value, self.python_class) or
                isinstance(value, self.__class__)):
            raise TypeError("'{0}' is not type of '{1}'".format(
                value, self.python_class
            ))

        object.__setattr__(self, '__storage__', value)

    def __eq__(self, value):
        return self.__storage__ == value

    def __len__(self):
        return len(self.__storage__)

    @classmethod
    def from_schema(cls, attrs):
        return attrs


class Object(JSONBase):

    schema_type = 'object'
    python_class = (dict, )

    def __init__(self, document):
        # FIXME remove when schema is enforced
        if getattr(self, '__schema__', {}).get('properties', None) is None:
            return  # there is nothing for us to do without schema

        for key, value in iteritems(document):
            field = getattr(self.__class__, key, None)

            if not isinstance(field, Field):
                raise RuntimeError("???")

            document[key] = field(value)
            object.__setattr__(self, key, document[key])

        super(Object, self).__init__(document)

    def __setattr__(self, key, value):
        field = getattr(self.__class__, key, None)
        if field is not None:
            self.__storage__[key] = field(value)
        else:
            self.__storage__[key] = value
        object.__setattr__(self, key, self.__storage__[key])

    def __getattr__(self, key):
        try:
            return self.__storage__[key]
        except KeyError:
            return super(Object, self).__getattr__(key)

    @classmethod
    def from_schema(cls, attrs):
        schema = attrs.get('__schema__', {})
        schema.setdefault('type', 'object')

        field_types = {name: attr.field_type for name, attr in iteritems(attrs)
                       if isinstance(attr, Field)}

        for key, value in iteritems(schema.get('properties', {})):
            if key in attrs:
                raise RuntimeError('Shall we continue?')
                continue
            attrs[key] = Field(schema_to_type(value))

        for name, field_type in iteritems(field_types):
            if hasattr(field_type, '__schema__'):
                attr_schema = field_type.__schema__
            else:
                attr_schema = {'type': field_type.schema_type}
            schema.setdefault('properties', {})
            schema['properties'][name] = attr_schema

        attrs['__schema__'] = schema
        return attrs


class List(JSONBase):

    schema_type = 'array'
    python_class = (list, tuple)

    def __init__(self, document, *args, **kwargs):
        items = kwargs.get('items', [])

        if len(items) == 1:
            document = [items[0](value) for value in document]
        elif len(items) > 1:
            raise NotImplemented("TODO multiple types")
        super(List, self).__init__(document)


    def __call__(self, value):
        wrapped = super(List, self).__call__(value)

        # FIXME remove when schema is enforced
        if self.schema is None:
            return wrapped

        for index, value in enumerate(wrapped.data):
            wrapped.data[index] = self.schema(value)
        return wrapped


class String(JSONBase):

    schema_type = 'string'
    python_class = (str, unicode)

# TODO implement Datetime


class Integer(JSONBase):

    schema_type = 'integer'
    python_class = (int, long)

# TODO implement Number


class Boolean(JSONBase):

    schema_type = 'boolean'
    python_class = (bool, )
