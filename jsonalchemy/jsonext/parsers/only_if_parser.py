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
    DecoratorBeforeEvalBaseExtensionParser


class OnlyIfParser(DecoratorBeforeEvalBaseExtensionParser):

    """
    Handle the ``@only_if`` decorator.

    .. code-block:: ini

        number_of_copies:
            creator:
                @only_if('BOOK' in self.get('collection.primary', []))
                get_number_of_copies(self.get('recid'))
    """

    __parsername__ = 'only_if'

    @classmethod
    def parse_element(cls, indent_stack):
        return (Keyword("@only_if").suppress() +
                originalTextFor(nestedExpr())
                ).setResultsName("only_if").setParseAction(
                    lambda toks: toks[0])

    @classmethod
    def create_element(cls, rule, field_def, content, metadata):
        return compile(content, '', 'eval')

    @classmethod
    def evaluate(cls, reader, args):
        """Evaluate parser.

        This is a special case where the real evaluation of the decorator
        is happening before the evaluation.
        """
        evaluated = try_to_eval(
            args, reader.metadata.functions,
            self=reader._json)
        if not isinstance(evaluated, (list, tuple)):
            return evaluated
        else:
            return all(evaluated)

parser = OnlyIfParser
