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

"""Test wrappers."""

import pytest

from jsonalchemy.wrappers import (
    List, String, Object, Integer
)


def test_simple_string_wrapper():
    """Test simple wrapping of String."""
    author = String()
    ellis = author("Ellis, J")

    assert ellis == 'Ellis, J'

    clone_ellis = author(ellis)

    assert clone_ellis == ellis


def test_simple_list_wrapper():
    """Test simple wrapping of String."""
    authors = List()
    nobles = authors(["Ellis, J", "Higgs, P"])

    assert len(nobles) == 2

    tuple_nobles = authors(("Ellis, J", "Higgs, P"))
    assert len(tuple_nobles) == 2

    with pytest.raises(TypeError) as excinfo:
        authors("Ellis, J")

    assert "is not type of" in str(excinfo.value)

def test_simple_integer_wrapper():
    """Test simple wrapping of String."""
    identifier = Integer()
    my_id = identifier(1)

    assert my_id > 0
    assert my_id < 2
    assert my_id <= 1
    assert my_id >= 1
    assert my_id == 1
    assert my_id != 0

    with pytest.raises(TypeError) as excinfo:
        identifier("1")

    assert "is not type of" in str(excinfo.value)


def test_simple_object_wrapper():
    """Test simple wrapping of String."""
    author = Object()
    ellis = author({
        "full_name": "Ellis, John R."
    })

    assert ellis == {
        "full_name": "Ellis, John R."
    }

    with pytest.raises(TypeError) as excinfo:
        author("Ellis, John R.")

    assert "is not type of" in str(excinfo.value)
