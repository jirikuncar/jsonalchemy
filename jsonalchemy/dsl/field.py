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
from six import iteritems, add_metaclass

from .creator import CreatorMixin
from .schema import SchemaMixin


class Field(CreatorMixin, SchemaMixin):

    name = None

    def _to_python(self, data):
        """Iternal data conversion."""
        return data

    def to_python(self, data):
        """Convert data to corresponding Python type."""
        if isinstance(data, list):
            data[:] = map(self._to_python, data)
            return data
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
