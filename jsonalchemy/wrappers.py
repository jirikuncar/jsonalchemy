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
from six import iteritems, add_metaclass


class Wrapper(object):

    def __init__(self, schema, data):
        self.schema = schema
        self.data = data

    def __eq__(self, other):
        return self.data == other

    def __le__(self, other):
        return self.data <= other

    def __lt__(self, other):
        return self.data < other

    def __gt__(self, other):
        return self.data > other

    def __ge__(self, other):
        return self.data >= other

    def __getattr__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return super(Wrapper, self).__getattr__(key)

    def __setattr__(self, key, value):
        if key in ('schema', 'data'):
            super(Wrapper, self).__setattr__(key, value)
        else:
            if hasattr(self.__class__, key):
                super(Wrapper, self).__setattr__(key, value)
            else:
                self.data[key] = getattr(self.schema, key)(value)

    def __setitem__(self, key, value):
        self.data[key] = getattr(self.schema, key)(value)

    def __getitem__(self, index):
        return self.data[index]

    def __delitem__(self, index):
        del self.data[index]

    def __len__(self):
        return len(self.data)

    def __nonzero__(self):
        return bool(self.data)


class MetaSchema(type):

    __schema_registry__ = {}

    def __new__(cls, name, bases, attrs):
        Meta = attrs.get('Meta', None)
        if Meta:
            schema = getattr(Meta, '__schema__', {})
            # TODO cls.__doc__ to title if not there
            schema_type = schema.get('type', None)
            if schema_type:
                Meta = cls.__schema_registry__[schema_type].from_schema(Meta)

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


def create_type_from_schema(schema, bases=()):
    schema_type = schema['type']
    schema_base = MetaSchema.__schema_registry__[schema_type]

    return type('Object', bases + (schema_base, ), {
        'Meta': type('Meta', (object, ), {
            '__schema__': schema
        }),
    })


def schema_to_type(schema):
    schema_type = schema.get('type', None)
    if schema_type in set(['object', 'list']):
        return create_type_from_schema(schema)()
    return MetaSchema.__schema_registry__[schema_type]()


@add_metaclass(MetaSchema)
class JSONBase(object):

    def __call__(self, value):
        wrapper_class = (
            getattr(self.Meta, 'Wrapper', Wrapper)
            if hasattr(self, 'Meta') else Wrapper
        )
        if isinstance(value, self.python_class):
            return wrapper_class(self, value)
        elif isinstance(value, wrapper_class):
            return value
        raise TypeError("'{0}' is not type of '{1}'".format(
            value, self.python_class
        ))


class Object(JSONBase):

    schema_type = 'object'
    python_class = (dict,)

    def __call__(self, value):
        wrapped = super(Object, self).__call__(value)

        # FIXME remove when schema is enforced
        if not hasattr(wrapped.schema, 'Meta'):
            return wrapped

        for key, value in iteritems(wrapped.data):
            if not hasattr(wrapped.schema.Meta, key):
                raise
            # recursively wrap all values
            wrapped.data[key] = getattr(wrapped.schema.Meta, key)(value)

        return wrapped

    def __getattr__(self, name):
        try:
            return super(Object, self).__getattr__(name)
        except AttributeError:
            return getattr(self.Meta, name)

    @classmethod
    def from_schema(cls, Meta):
        for key, value in iteritems(Meta.__schema__.get('properties', {})):
            setattr(Meta, key, schema_to_type(value))

        return Meta


class List(JSONBase):

    schema_type = 'array'
    python_class = (list, tuple)

    def __init__(self, schema=None):
        if schema and isinstance(schema, type):
            self.schema = schema()
        else:
            self.schema = schema

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

    @classmethod
    def from_schema(cls, Meta):
        return Meta

# TODO implement Datetime


class Integer(JSONBase):

    schema_type = 'integer'
    python_class = (int, long)

# TODO implement Number


class Boolean(JSONBase):

    schema_type = 'boolean'
    python_class = (bool, )
