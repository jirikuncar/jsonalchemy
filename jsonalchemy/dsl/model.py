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

"""JSONAlchemy DSL Model."""

import re

from six import iteritems, add_metaclass

from .field import Field
from .base import Base, MODEL_ATTR, model_attr


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def underscorify(name):
    """Generate underscored lowercased name from camel cased name."""
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


class Metadata(dict):

    def __init__(self, name, *args, **kwargs):
        self._name = name
        self.properties = {}
        return super(Metadata, self).__init__(*args, **kwargs)

    def field(self, name, value):
        self.properties[name] = value


class ModelTypeMeta(type):
    """Define meta-class that keeps track about all its subclasses."""

    def __new__(cls, name, bases, attrs):
        """Keep track about all model fields and other metadata."""
        attrs[MODEL_ATTR] = ModelTypeOptions(name, bases, attrs)
        return super(ModelTypeMeta, cls).__new__(cls, name, bases, attrs)

    def __getattr__(cls, name):
        try:
            return super(ModelTypeMeta, cls).__getattr__(name)
        except AttributeError:
            try:
                return model_attr(cls).metadata.properties[name]
            except KeyError:
                raise AttributeError(name)


class ModelTypeOptions(object):

    def __init__(self, name, bases, attrs):
        model_name = underscorify(name)
        self.metadata = Metadata(model_name)

        # register all declared fields into the metadata
        for name, value in list(iteritems(attrs)):
            if isinstance(value, Field):
                self.metadata.field(name, value)
                del attrs[name]

        # model inheritance
        # - include the fields from parents' metadata
        for base in bases:
            options = model_attr(base)
            if options is not None and hasattr(options, 'metadata'):
                self.metadata.update(options.metadata, update_only=True)
            else:
                for name in dir(base):
                    value = getattr(base, name, None)
                    if isinstance(value, Field):
                        self.metadata.field(name, value)


@add_metaclass(ModelTypeMeta)
class Model(Base):

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
