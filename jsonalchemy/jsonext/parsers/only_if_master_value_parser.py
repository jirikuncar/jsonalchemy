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

from pyparsing import Keyword, originalTextFor, nestedExpr

from jsonalchemy.utils import try_to_eval

from jsonalchemy.parser import \
    DecoratorOnEvalBaseExtensionParser


class OnlyIfMasterValueParser(DecoratorOnEvalBaseExtensionParser):

    """
    Handle the ``@only_if_master_value`` decorator.

    .. code-block:: ini

        files_to_upload:
            creator:
                @only_if_value(is_local_url(value['u']),
                               is_available_url(value['u']))
                marc, "8564_", {'hots_name': value['a'],
                                'access_number': value['b'],
                        ........
    """

    __parsername__ = 'only_if_master_value'

    @classmethod
    def parse_element(cls, indent_stack):
        """Set ``only_if_master_value`` attribute to the rule."""
        return (Keyword("@only_if_master_value").suppress() +
                originalTextFor(nestedExpr())
                ).setResultsName("only_if_master_value").setParseAction(
                    lambda toks: toks[0])

    @classmethod
    def create_element(cls, rule, field_def, content, metadata):
        """Simply return the list of boolean expressions."""
        return compile(content, '', 'eval')

    @classmethod
    def evaluate(cls, value, metadata, args):
        """Evaluate ``args`` with the master value from the input.

        :returns: a boolean depending on evaluated ``value``.
        """
        evaluated = try_to_eval(args, metadata.functions, value=value)
        if not isinstance(evaluated, (list, tuple)):
            return evaluated
        else:
            return all(evaluated)

parser = OnlyIfMasterValueParser
