# -*- coding: utf-8 -*-
#
# This file is part of JSONAlchemy.
# Copyright (C) 2013, 2014, 2015 CERN.
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

"""Cerberus validator.

See (Cerberus documentation)[http://cerberus.readthedocs.org/en/latest]
"""
import datetime
import collections
import re
import six

from cerberus import Validator as ValidatorBase
from cerberus import errors


class Validator(ValidatorBase):

    """Cerberus validator."""

    def __init__(self, schema=None, transparent_schema_rules=True,
                 ignore_none_values=False, allow_unknown=True):
        """Same as in Cerberus."""
        super(Validator, self).__init__(schema, transparent_schema_rules,
                                        ignore_none_values, allow_unknown)

    # FIXME: refactor spaghetti code
    @staticmethod
    def force_type(document, field, type_):
        """Force `field` content to `type`."""
        if type_ == 'list' and not isinstance(document[field], (list, tuple)):
            document[field] = [document[field], ]
        elif type_ == 'string' and not isinstance(document[field],
                                                  six.string_types):
            document[field] = str(document[field])
        elif type_ == 'boolean' and not isinstance(document[field], bool):
            document[field] = bool(document[field])
        elif type_ == 'integer' and not isinstance(document[field], int):
            document[field] = int(document[field])
        elif type_ == 'datetime' and not isinstance(document[field], datetime):
            from dateutil import parser
            document[field] = parser.parse(document[field])
        else:
            document[field] = eval(type_)(document[field])

    def _validate_type_objectid(self, field, value):
        """Enable validation for `objectid` schema attribute.

        :param field: field name.
        :param value: field value.
        """
        if not re.match('[a-f0-9]{24}', value):
            self._error(field, errors.ERROR_BAD_TYPE % 'ObjectId')

    def _validate_type_uuid(self, field, value):
        """Enable validation for `uuid.uuid4()` schema attribute.

        :param field: field name.
        :param value: field value.
        """
        if not re.match('[a-f0-9\-]{36}', value):
            self._error(field, errors.ERROR_BAD_TYPE % 'UUID')
