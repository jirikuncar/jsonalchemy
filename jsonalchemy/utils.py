# -*- coding: utf-8 -*-
#
# This file is part of JSONAlchemy.
# Copyright (C) 2014, 2015 CERN.
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

"""Utility functions."""

import functools
import importlib
import os
import six


def try_to_eval(string, context={}, **general_context):
    """Take care of evaluating the python expression.

    If an exception happens, it tries to import the needed module.

    :param string: String to evaluate
    :param context: Context needed, in some cases, to evaluate the string

    :return: The value of the expression inside string
    """
    if not string:
        return None

    res = None
    imports = []
    general_context.update(context)
    simple = False
    while True:
        try:
            # kwalitee: disable=eval
            res = eval(string, globals().update(general_context), locals())
        except NameError as err:
            # Try first to import using werkzeug import_string
            try:
                if "." in string:
                    part = string.split('.')[0]
                    importlib.import_module(part)
                    for i in string.split('.')[1:]:
                        part += '.' + i
                        importlib.import_module(part)
                    continue
                else:
                    simple = True
            except:
                pass

            import_name = str(err).split("'")[1]
            if import_name not in imports:
                if import_name in context:
                    globals()[import_name] = context[import_name]
                else:
                    globals()[import_name] = __import__(import_name)
                    imports.append(import_name)
                continue
            elif simple:
                import_name = str(err).split("'")[0]
                if import_name in context:
                    globals()[import_name] = context[import_name]
                else:
                    globals()[import_name] = __import__(import_name)
                    imports.append(import_name)
                continue

            raise ImportError("Can't import the needed module to evaluate %s"
                              (string, ))
        if isinstance(res, type(os)):
            raise ImportError
        return res


def filter_values(f):
    """Remove None values from dictionary."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        out = f(*args, **kwargs)
        return dict((k, v) for k, v in six.iteritems(out) if v is not None)
    return wrapper


def for_each_value(f):
    """Apply function to each item."""
    @functools.wraps(f)
    def wrapper(self, values, **kwargs):
        if isinstance(values, list):
            return [f(self, value, **kwargs) for value in values]
        return f(self, values, **kwargs)
    return wrapper
