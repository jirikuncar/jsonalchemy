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

"""Test model creation."""

from datetime import datetime

from jsonalchemy import dsl


def get_simple_record():

    class Record(dsl.Model):

        """Represent a record model."""

        id = dsl.Field()
        title = dsl.Field()

    return Record

def get_record_and_mixin():
    class Mixin(object):
        id = dsl.Field()


    class Record(Mixin, dsl.Model):

        """Represent a record model."""

        title = dsl.Field()

    return Record, Mixin


def test_model_metadadata():
    Record = get_simple_record()

    assert hasattr(Record, '_model_type')
    assert len(Record._model_type.metadata.properties) == 2


def test_model_mixin():
    Record, _ = get_record_and_mixin()

    assert hasattr(Record, '_model_type')
    assert len(Record._model_type.metadata.properties) == 2


def test_model_instance():
    Record = get_simple_record()

    record = Record()
    record.id = 1
    assert record.id == 1
    assert getattr(record, 'title', None) is None

    record = Record(id=2, title='Test')
    assert record.id == 2
    assert record.title == 'Test'
    assert getattr(record, 'foo', '_foo_') == '_foo_'


def test_model_creation():
    from jsonalchemy.dsl.creator import translate, _clean_index

    class Record(dsl.Model):

        """Represent a record model."""

        id = dsl.Field()
        title = dsl.Field()

        @title.creator('marc', '245__')
        def title(self, value):
            return value['a']

    record = translate(Record, {'245__': {'a': 'Test'}}, 'marc')
    assert record.title == 'Test'

    record = translate(Record, {'001__': 1}, 'marc')
    assert 'id' not in record.to_dict()

    # NOTE cleaning cache is necessary after class is modified
    _clean_index(Record)

    Record.id.creator('marc', '001__')(
        lambda self, value: value
    )
    record = translate(Record, {'001__': 1}, 'marc')
    assert record.id == 1


def test_model_schema():
    from jsonalchemy.dsl.schema import get_schema

    class Record(dsl.Model):

        """Represent a record model."""

        id = dsl.Field()
        modification_date = dsl.Field()

        @modification_date.schema
        def modification_date(self):
            return {
                'type': 'datetime',
                'required': True,
                'default': datetime.now,
            }

    record = Record()
    assert record.modification_date <= datetime.now()
    assert getattr(record, 'id', None) == None

    schema = get_schema(Record)
    assert 'modification_date' in schema
    assert 'id' not in schema

def test_field_composability():

    class Record(dsl.Model):

        """Represent a record model."""

        id = dsl.Field()
        title = dsl.Object(
            title=dsl.Field(),
            subtitle=dsl.Field(),
        )
        level1 = dsl.Object(
            attr1=dsl.Field(),
            level2=dsl.Object(
                attr2=dsl.Field()
            )
        )
        author = dsl.Object(
            name=dsl.Field(),
            affiliation=dsl.Field(),
        )
        keywords = dsl.List(
            dsl.Object(
                value=dsl.Field(),
            )
        )

        @author.creator('marc', '100__')
        def author(self, value):
            return {'name': value['a'], 'affiliation': value['f']}

    record = Record()
    record.title.title = 'Test'
    record.title.subtitle = 'Subtest'
    record.level1.attr1 = 'A1'
    record.level1.level2.attr2 = 'A2'
    record.author = {'name': 'Ellis', 'affiliation': 'CERN'}
    record.keywords.append(dict(value='kw1'))

    assert record.author.name == 'Ellis'
    assert record.author.affiliation == 'CERN'
    assert record.keywords[0].value == 'kw1'

    record.keywords[0].value = 'kw2'

    out = record.to_dict()
    assert out['title']['title'] == 'Test'
    assert out['title']['subtitle'] == 'Subtest'
    assert out['level1']['level2']['attr2'] == 'A2'
    assert out['keywords'][0]['value'] == 'kw2'

    from jsonalchemy.dsl.creator import translate
    record = translate(Record, {'100__': {'a': 'Ellis', 'f': 'CERN'}}, 'marc')
    assert record.author.name == 'Ellis'
    assert record.author.affiliation == 'CERN'

    record = Record(id=1, author=dict(name='Ellis', affiliation='CERN'))
    assert record.id == 1
    assert record.author.name == 'Ellis'
    assert record.author.affiliation == 'CERN'
