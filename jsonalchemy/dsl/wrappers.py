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

"""List and dictionary attribute wrappers."""


def _wrap(val):
    """Wrap value to ``AttrDict`` or ``AttrList`` class."""
    if isinstance(val, dict) and not isinstance(val, AttrDict):
        return AttrDict(val)
    if isinstance(val, list) and not isinstance(val, AttrList):
        return AttrList(val)
    return val


class AttrList(object):
    """Helper class for accessing list by attributes."""

    def __init__(self, l):
        # make iteables into lists
        if not isinstance(l, list):
            l = list(l)
        self._l_ = l

    def __repr__(self):
        return repr(self._l_)

    def __eq__(self, other):
        if isinstance(other, AttrList):
            return other._l_ == self._l_
        # make sure we still equal to a dict with the same data
        return other == self._l_

    def __getitem__(self, k):
        l = self._l_[k]
        if isinstance(k, slice):
            return AttrList(l)
        return _wrap(l)

    def __iter__(self):
        return map(_wrap, self._l_)

    def __len__(self):
        return len(self._l_)

    def __nonzero__(self):
        return bool(self._l_)
    __bool__ = __nonzero__

    def __getattr__(self, name):
        return getattr(self._l_, name)


class AttrDict(object):
    """Helper class to provide attribute like R/W access to dictionaries.

    Used to provide a convenient way to access both results and nested dsl
    dicts.
    """

    def __init__(self, d):
        # assign the inner dict manually to prevent __setattr__ from firing
        super(AttrDict, self).__setattr__('_d_', d)

    def __contains__(self, key):
        return key in self._d_

    def __nonzero__(self):
        return bool(self._d_)
    __bool__ = __nonzero__

    def __dir__(self):
        # introspection for auto-complete in IPython etc
        return list(self._d_.keys())

    def __eq__(self, other):
        if isinstance(other, AttrDict):
            return other._d_ == self._d_
        # make sure we still equal to a dict with the same data
        return other == self._d_

    def __repr__(self):
        r = repr(self._d_)
        if len(r) > 60:
            r = r[:60] + '...}'
        return r

    def get(self, key, default=None):
        # Don't confuse `obj.get('...')` as `obj['get']`.
        try:
            return self._d_[key]
        except KeyError:
            return default

    def __getattr__(self, attr_name):
        try:
            return _wrap(self._d_[attr_name])
        except KeyError:
            raise AttributeError('%r object has no attribute %r' % (
                self.__class__.__name__, attr_name))

    def __getitem__(self, key):
        # don't wrap things whe accessing via __getitem__ for consistency
        return self._d_[key]

    def __setitem__(self, key, value):
        self._d_[key] = value
    __setattr__ = __setitem__

    def __iter__(self):
        return iter(self._d_)

    def iteritems(self):
        from six import iteritems
        return iteritems(self._d_)
