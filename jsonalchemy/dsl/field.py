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
from .schema import SchemaMixin
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

    def _to_python(self, data):
        if isinstance(data, date):
            return data
        try:
            # TODO: add format awareness
            return parser.parse(data)
        except (TypeError, ValueError):
            raise  # XXX


class Object(Field):

    name = 'object'

    def __init__(self, *args, **kwargs):
        from .model import Model
        if len(args) == 1 and len(kwargs) == 0:
            assert isinstance(args[0], dict)
            kwargs = args[0]

        self._model = type('Object', (Model, ), kwargs)
        self._data = self._model()

    def default(self):
        return self._data

    def __getattr__(self, name):
        if name in ('_data', '_model'):
            return super(Object, self).__getattr__(name)
        return getattr(self._data, name)

    def __setattr__(self, name, value):
        if name in ('_data', '_model'):
            return super(Object, self).__setattr__(name, value)
        return setattr(self._data, name, value)


class List(Field, list):

    name = 'list'

    def __init__(self, model):
        self._model = model
        self._data = None

    def default(self):
        return []

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        if not isinstance(value, self._model):
            value = self._model(value)
        self._data[index] = value

    def __len__(self):
        return len(self._data)

    def _to_python(self, data):
        if isinstance(data, list):
            data[:] = map(self._model.to_python, data)
            return data
        return self._model.to_python(data)
