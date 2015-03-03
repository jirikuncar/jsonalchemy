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

"""Base objects."""

# from attrdict import AttrDict
from six import iteritems

from .wrappers import AttrDict, AttrList

MODEL_ATTR = '_model_type'


def model_attr(cls):
    """Shortcut to retrieve model options."""
    return getattr(cls, MODEL_ATTR, None)


def _make_dsl_class(base, name, params_def=None):
    """Generate a DSL class based on the name of the DSL object."""
    attrs = {'name': name}
    if params_def:
        attrs['_param_defs'] = params_def
    cls_name = str(''.join(s.title() for s in name.split('_')))
    return type(cls_name, (base, ), attrs)


class Base(AttrDict):

    def __init__(self, **kwargs):
        """Instanciate AttrDict using custom ``__setattr__`` method."""
        super(Base, self).__init__({})
        for (k, v) in iteritems(kwargs):
            setattr(self, k, v)

    def __getattr__(self, name):
        properties = model_attr(self.__class__).metadata.properties
        try:
            if name in properties:
                field = properties[name]
                if hasattr(field, '_wrap'):
                    try:
                        return field._wrap(self._d_[name])
                    except KeyError:
                        pass
            return super(Base, self).__getattr__(name)
        except AttributeError:
            if name in properties:
                field = properties[name]
                if hasattr(field, 'default'):
                    setattr(self, name, field.default())
                    return getattr(self, name)
            raise

    def __setattr__(self, name, value):
        properties = model_attr(self.__class__).metadata.properties
        if name in properties:
            value = properties[name].to_python(value)
        super(Base, self).__setattr__(name, value)

    def to_dict(self, value=None):
        value = value or self._d_
        out = {}
        properties = model_attr(self.__class__).metadata.properties
        for k, v in iteritems(value):
            to_dict = getattr(properties[k], 'to_dict', None)
            if isinstance(v, (list, tuple)):
                v = [to_dict(i) if to_dict else i for i in v]
            else:
                v = to_dict(v) if to_dict else v
            out[k] = v
        return out
