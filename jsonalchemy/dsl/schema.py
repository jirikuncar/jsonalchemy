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

"""JSONAlchemy schema extension."""

from six import iteritems

from .base import model_attr

# FIXME move to jsonalchemy.ext.schema


class SchemaMixin(object):

    """Creator Mixin."""

    def __init__(self, *args, **kwargs):
        _schema = kwargs.pop('schema', None)
        if _schema is not None:
            self.schema(_schema)

        super(SchemaMixin, self).__init__(*args, **kwargs)

    def schema(self, rule):
        """Register schema rule."""
        _schema = getattr(self, '_schema', dict())
        _schema.update(rule(self) if callable(rule) else rule)
        setattr(self, '_schema', _schema)

        if 'default' in _schema:
            _default = _schema['default']

            def default():
                """Return default value from schema."""
                return _default() if callable(_default) else _default

            self.default = default

        return self


def get_schema(cls):
    """Collect schema for all fields from given model."""
    def generator():
        for name, field in iteritems(model_attr(cls).metadata.properties):
            try:
                yield name, field._schema
            except AttributeError:
                yield name, {'title': name}

    return {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': cls.__name__,
        'description': getattr(cls, __doc__, ''),
        'properties': dict(generator()),
    }
