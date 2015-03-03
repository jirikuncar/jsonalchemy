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

"""JSONAlchemy DSL Field."""

import functools
import re

from datetime import date
from dateutil import parser
from six import iteritems

from .creator import CreatorMixin
from .schema import SchemaMixin, get_schema
from .wrappers import AttrDict


class Field(CreatorMixin, SchemaMixin):

    name = None

    def _to_python(self, data):
        """Iternal data conversion."""
        return data

    def to_python(self, data):
        """Convert data to corresponding Python type."""
        return self._to_python(data)


class Date(Field):

    name = 'date'
    _schema = {'type': 'date'}

    def _to_python(self, data):
        if isinstance(data, date) or data is None:
            return data
        try:
            # TODO: add format awareness
            return parser.parse(data)
        except (TypeError, ValueError, AttributeError):
            raise  # XXX

    def to_dict(self, value):
        if value:
            return value.isoformat()
        return value


class Object(Field):

    name = 'object'

    def __init__(self, *args, **kwargs):
        from .model import Model
        if len(args) == 1 and len(kwargs) == 0:
            assert isinstance(args[0], dict)
            kwargs = args[0]

        self._model = type('Object', (Model, ), kwargs)
        self._schema = {
            'type': 'object',
            'properties': get_schema(self._model),
        }

    def default(self):
        return {}

    def __getattr__(self, name):
        if name in ('_data', '_model', '_schema'):
            return super(Object, self).__getattr__(name)
        return getattr(self._model, name)

    def __setattr__(self, name, value):
        if name in ('_data', '_model', '_schema'):
            return super(Object, self).__setattr__(name, value)
        return setattr(self._model, name, value)

    def _to_python(self, data):
        if not isinstance(data, self._model):
            data = self._model(data)
        return data


def _wrap_list(model, data):
    class WrapList(object):

        def __init__(self, obj):
            self.obj = obj

        def __getitem__(self, index):
            value = self.obj.__getitem__(index)
            value = model.to_python(value)
            return value

        def __setitem__(self, index, value):
            value = model.to_python(value)
            return self.obj.__setitem__(index, value)

        def append(self, value):
            value = model.to_python(value)
            return self.obj.append(value)

        def __len__(self):
            return len(self.obj)

    if type(data) == list:
        return WrapList(data)
    return data


class List(Field):

    name = 'list'

    def __init__(self, model):
        self._model = model
        self._schema = {
            'type': 'array',
            'items': (
                get_schema(self._model) if not isinstance(self._model, Field)
                else getattr(self._model, '_schema', {})
            ),
        }

    def default(self):
        return []

    def _wrap(self, data):
        return _wrap_list(self._model, data)

    def _to_python(self, data):
        if isinstance(data, list):
            data[:] = map(self._model.to_python, data)
            return _wrap_list(self._model, data)
        raise TypeError("Invalid data type '{0} - list required.".format(
            type(data)))
