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

import importlib

from pyparsing import (
    Keyword, OneOrMore, quotedString, removeQuotes, restOfLine,
)

from jsonalchemy.utils import try_to_eval
from jsonalchemy.parser import (
    ModelBaseExtensionParser, indentedBlock,
)


class ExtensionModelParser(ModelBaseExtensionParser):  # pylint: disable=W0232
    """Handle the extension section in the model definitions.

    .. code-block:: text

        fields:
            ....
            extensions:
                'invenio.modules.records.api:RecordIter'
                'jsonalchemy.bases:Versinable'

    """

    __parsername__ = 'extensions'

    @classmethod
    def parse_element(cls, indent_stack):
        """Set ``extensions`` attribute to the rule definition."""
        import_line = quotedString.setParseAction(removeQuotes) + restOfLine
        return (Keyword('extensions:').suppress() +
                indentedBlock(OneOrMore(import_line), indent_stack)
                ).setResultsName('extensions')

    @classmethod
    def create_element(cls, rule, metadata):  # pylint: disable=W0613
        """Simply return the list of extensions."""
        return [e.strip() for e in rule.extensions.asList() if e]

    @classmethod
    def inherit_model(cls, current_value, base_value):
        """Extend list of extensions with the new ones without repeating."""
        if current_value is None:
            return base_value
        elif base_value is None:
            return current_value
        return list(set(base_value + current_value))

    @classmethod
    def extend_model(cls, current_value, new_value):
        """Like inherit."""
        return cls.inherit_model(current_value, new_value)

    @classmethod
    def add_info_to_field(cls, info):
        """Adds the list of extensions to the model information."""
        return info

    @classmethod
    def evaluate(cls, obj, args):
        """Extend the incoming object with all the new things from args."""
        if args is None:
            return
        extensions = []
        for ext in args:
            try:
                if ':' in ext:
                    package, attr = ext.split(':')
                else:
                    package, attr = ext.rsplit('.', 1)
                extensions.append(
                    getattr(importlib.import_module(package), attr)
                )
            except (ImportError, AttributeError, KeyError):
                extensions.append(try_to_eval(ext))
        extensions.append(obj.__class__)

        obj.__class__ = type(obj.__class__.__name__, tuple(extensions), {})

parser = ExtensionModelParser
