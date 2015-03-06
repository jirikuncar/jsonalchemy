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

import pytest

from datetime import datetime

from jsonalchemy import dsl


def get_simple_record():

    class Record(dsl.Model):

        """Represent a record model."""

        id = dsl.Field()
        title = dsl.Field()
        publication_date = dsl.Date()

    return Record

def get_record_and_mixin():
    class Mixin(object):
        id = dsl.Field()
        publication_date = dsl.Date()


    class Record(Mixin, dsl.Model):

        """Represent a record model."""

        title = dsl.Field()

    return Record, Mixin


def test_model_metadadata():
    Record = get_simple_record()

    assert hasattr(Record, '_model_type')
    assert len(Record._model_type.metadata.properties) == 3


def test_model_mixin():
    Record, _ = get_record_and_mixin()

    assert hasattr(Record, '_model_type')
    assert len(Record._model_type.metadata.properties) == 3


def test_model_instance():
    Record = get_simple_record()

    publication_date = datetime.now()

    record = Record()
    record.id = 1
    record.publication_date = publication_date
    assert record.id == 1
    assert getattr(record, 'title', None) is None
    assert record.to_dict()['publication_date'] == publication_date.isoformat()

    record.publication_date = publication_date.isoformat()
    assert record.to_dict()['publication_date'] == publication_date.isoformat()

    with pytest.raises(ValueError) as excinfo:
        record.publication_date = 'deadbeef'
        assert 'unknown string format' in str(extinfo.value)

    record.publication_date = None
    assert record.to_dict()['publication_date'] == None

    record = Record(id=2, title='Test',
                    publication_date=publication_date.isoformat())
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
        def title(self, key, value):
            return value['a']

    record = translate(Record, {'245__': {'a': 'Test'}}, 'marc')
    assert record.title == 'Test'

    record = translate(Record, {'001__': 1}, 'marc')
    assert 'id' not in record.to_dict()

    # NOTE cleaning cache is necessary after class is modified
    _clean_index(Record)

    Record.id.creator('marc', '001__')(
        lambda self, key, value: value
    )
    record = translate(Record, {'001__': 1}, 'marc')
    assert record.id == 1


def test_model_schema():
    from jsonalchemy.dsl.schema import get_schema

    class Record(dsl.Model):

        """Represent a record model."""

        id = dsl.Field()
        modification_date = dsl.Field()
        title = dsl.Field(schema={'type': 'string', 'required': True})

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

    schema = get_schema(Record)['properties']
    assert schema['id']['title'] == 'id'
    assert 'modification_date' in schema
    assert 'title' in schema

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
                dict(attr2=dsl.Field())
            )
        )
        author = dsl.Object(
            name=dsl.Field(),
            affiliation=dsl.Field(),
            birthday=dsl.Date(),
        )
        keywords = dsl.List(
            dsl.Object(
                value=dsl.Field(),
                created=dsl.Date(schema=dict(default=datetime.now)),
            )
        )

        @author.creator('marc', '100__')
        def author(self, key, value):
            return {'name': value['a'], 'affiliation': value['f']}

    record = Record()
    record.title.title = 'Test'
    record.title.subtitle = 'Subtest'
    record.level1.attr1 = 'A1'
    record.level1.level2.attr2 = 'A2'
    record.author = {'name': 'Ellis', 'affiliation': 'CERN',
                     'birthday': '1960-01-02'}
    record.keywords.append(dict(value='kw1'))
    record.keywords.append(dict(value='kw2'))

    with pytest.raises(TypeError) as excinfo:
        record.keywords = 'deadbeef'

    assert record.author.name == 'Ellis'
    assert record.author.affiliation == 'CERN'
    assert isinstance(record.author.birthday, datetime)
    assert len(record.keywords) == 2
    assert record.keywords[0].value == 'kw1'
    assert record.keywords[0].created is not None
    assert record.keywords[0].created <= record.keywords[1].created

    record.keywords[0].value = 'kw1_1'
    record.keywords[1] = {'value': 'kw2_1'}

    out = record.to_dict()
    assert out['title']['title'] == 'Test'
    assert out['title']['subtitle'] == 'Subtest'
    assert out['level1']['level2']['attr2'] == 'A2'
    assert out['keywords'][0]['value'] == 'kw1_1'
    assert out['keywords'][1]['value'] == 'kw2_1'

    from jsonalchemy.dsl.creator import translate
    record = translate(Record, {'100__': {'a': 'Ellis', 'f': 'CERN'}}, 'marc')
    assert record.author.name == 'Ellis'
    assert record.author.affiliation == 'CERN'

    record = Record(id=1, author=dict(name='Ellis', affiliation='CERN'))
    assert record.id == 1
    assert record.author.name == 'Ellis'
    assert record.author.affiliation == 'CERN'

    assert isinstance(Record.keywords._model.created.default(), datetime)
    assert Record.level1._schema['type'] == 'object'


def test_list_composability():
    from jsonalchemy.dsl.schema import get_schema

    class Record(dsl.Model):

        """Represent a record model."""

        id = dsl.Field()
        keywords = dsl.List(
            dsl.Field(schema={'type': 'string'}),
        )
        dates = dsl.List(
            dsl.Date(schema=dict(default=datetime.now)),
        )

    record = Record(keywords=['kw1', 'kw2'], dates=[''])

    assert record.keywords[0] == 'kw1'
    assert record.keywords[1] == 'kw2'
    assert record.dates[0] <= datetime.now()

    schema = get_schema(Record)
    assert schema['properties']['keywords']['items']['type'] == 'string'
    assert schema['properties']['dates']['items']['type'] == 'date'


def test_marc21():
    from jsonalchemy.contrib.marc21 import Record
    from jsonalchemy.dsl.creator import translate
    from jsonalchemy.dsl.schema import get_schema

    record = translate(Record, {
        '001': '1',
        '100__': {'a': 'Ellis', 'u': 'CERN'},
        '020': [{'a': '80-902734-1-6'}, {'a': '960-425-059-0'}]
    }, 'marc')

    assert record.control_number == '1'
    assert record.main_entry_personal_name.personal_name == 'Ellis'
    assert record.main_entry_personal_name.affiliation == 'CERN'
    assert set(
        issn.international_standard_book_number
        for issn in record.international_standard_book_number
    ) == set(['80-902734-1-6', '960-425-059-0'])

    schema = get_schema(Record)['properties']
    assert schema['international_standard_book_number']['type'] == 'array'


def test_custom_model_property():

    def name(self):
        out = self.last_name
        if getattr(self, 'first_name', None):
            out += ', ' + self.first_name
        return out

    author_model = dsl.Object(
        first_name=dsl.Field(),
        last_name=dsl.Field(),
        name=dsl.hybrid_property(name),
        affiliation=dsl.Field(),
        birthday=dsl.Date(),
    )

    @author_model.name.setter
    def name(self, value):
        if ', ' in value:
            self.last_name, self.first_name = value.split(', ')
        else:
            self.last_name = value

    class Record(dsl.Model):
        first_author = author_model
        additional_authors = dsl.List(author_model)

        @dsl.hybrid_property
        def authors(self):
            return [self.first_author] + self.additional_authors

        @authors.setter
        def authors(self, value):
            self.first_author = value[0]
            self.additional_authors = value[1:]

    record = Record(
        first_author=dict(name='Ellis', affiliation='CERN'),
        additional_authors=[
            dict(name='Higgs', affiliation='CERN'),
            dict(name='Heuer', affiliation='CERN'),
        ],
    )

    assert len(record.authors) == 3

    record.authors[0].name = 'Ellis, J'
    record.authors[1].affiliation = 'DESY'
    record.authors[2].birthday = ''
    assert record.first_author.name == 'Ellis, J'
    assert record.additional_authors[0].affiliation == 'DESY'
    assert isinstance(record.additional_authors[1].birthday, datetime)

    authors = record.authors
    authors.append(dict(name='Einstein'))
    record.authors = authors
    assert record.additional_authors[-1].name == 'Einstein'
