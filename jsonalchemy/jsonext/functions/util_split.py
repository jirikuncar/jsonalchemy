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

"""Function for tokenizing strings in models' files."""


def util_split(string, separator, index):
    """
    Helper function to split safely a string and get the n-th element.

    :param string: String to be split
    :param separator:
    :param index: n-th part of the split string to return

    :return: The n-th part of the string or empty string in case of error
    """
    string_splitted = string.split(separator)
    try:
        return string_splitted[index].strip()
    except:
        return ""
