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

"""JSONAlchemy creator extension."""

from six import iteritems

from .base import model_attr

# FIXME move to jsonalchemy.ext.creator


def legacy(*rules):
    def decorator(f):
        setattr(f, '_legacy', rules)
        return f
    return decorator


class CreatorMixin(object):

    """Creator Mixin."""

    def creator(self, source_format, *source_tags):
        """Register creator rule."""
        def decorator(f):
            rule = getattr(self, '_creator_rule', dict())
            if source_format not in rule:
                rule[source_format] = list()
            rule[source_format].append((source_tags, f))
            setattr(self, '_creator_rule', rule)
            return self
        return decorator


def _build_index(cls, source_format):
    """Build string matching facilities for regular expressions."""
    import esmre
    index = esmre.Index()
    for name, field in iteritems(model_attr(cls).metadata.properties):
        if source_format in getattr(field, '_creator_rule', {}):
            for rule in reversed(field._creator_rule[source_format]):
                source_fields, creator = rule
                for source_field in source_fields:
                    index.enter(source_field, (name, field, creator))
    return index


def _clean_index(cls):
    """Clean index of creator rules."""
    setattr(cls, '_creator_index', dict())


def translate(cls, blob, source_format):
    """Translate blob values and instantiate new model instance."""
    index = getattr(cls, '_creator_index', dict())
    if source_format not in index:
        index[source_format] = _build_index(cls, source_format)
        setattr(cls, '_creator_index', index)

    rules = index[source_format]

    def generator():
        for key, value in iteritems(blob):
            for name, field, creator in rules.query(key):
                yield name, creator(field, value)

    return cls(**dict(generator()))
