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
            raise AttributeError


    def __getitem__(self, index):
        return self.data[index]

    def __delitem__(self, index):
        del self.data[index]

    def __len__(self):
        return len(self.data)

    def __nonzero__(self):
        return bool(self.data)


class MetaSchema(type):

    def __new__(cls, name, bases, attrs):
        return super(MetaSchema, cls).__new__(cls, name, bases, attrs)


@add_metaclass(MetaSchema)
class JSONBase(object):

    def __call__(self, value):
        if isinstance(value, self.python_class):
            return Wrapper(self, value)
        elif isinstance(value, Wrapper):
            return value
        raise TypeError("'{0}' is not type of '{1}'".format(
            value, self.python_class
        ))


class Object(JSONBase):

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


class List(JSONBase):

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

    python_class = (str, unicode)


class Integer(JSONBase):

    python_class = (int, long)


class Boolean(JSONBase):

    python_class = (bool, )
