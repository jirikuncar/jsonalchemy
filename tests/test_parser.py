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

"""Unit tests for the parser engine."""

import sys
import tempfile
import testext

from os.path import dirname, realpath
from testext import functions
from unittest import TestCase

from jsonalchemy.parser import (
    ModelParser, guess_legacy_field_names, get_producer_rules
)
from jsonalchemy.registry import MetaData

sys.path.append(dirname(realpath(__file__)))


class TestParser(TestCase):

    def setUp(self):
        self.metadata = MetaData(['jsonalchemy.jsonext', 'testext'])
        self.model_parser = ModelParser(self.metadata)
        self.field_parser = self.model_parser.field_parser

    def test_wrong_indent(self):
        """JSONAlchemy - wrong indent"""
        from jsonalchemy.parser import _create_field_parser
        import pyparsing
        parser = _create_field_parser(self.metadata)
        test = """
        foo:
            creator:
        bar, '1', foo()
        """
        self.assertRaises(pyparsing.ParseException, parser.parseString, test)

        from jsonalchemy.errors import FieldParserException
        tmp_file = tempfile.NamedTemporaryFile()
        config = """
        foo:
            creator:
        bar, '1', foo()
        """
        tmp_file.write(config)
        tmp_file.flush()

        self.metadata.fields.append(tmp_file.name)

        self.assertRaises(
            FieldParserException, self.field_parser.reparse)
        tmp_file.close()

    def test_wrong_field_definitions(self):
        """JSONAlchemy - wrong field definitions"""
        from jsonalchemy.errors import FieldParserException
        tmp_file_4 = tempfile.NamedTemporaryFile()
        config_4 = '''
        title:
            creator:
                marc, '245__', value
        '''
        tmp_file_4.write(config_4)
        tmp_file_4.flush()

        fields = list(self.metadata.fields)
        fields.append(tmp_file_4.name)
        self.metadata._cache_fields = fields
        self.assertRaises(
            FieldParserException, self.field_parser.reparse)
        tmp_file_4.close()

    def test_wrong_field_inheritance(self):
        """JSONAlchmey - not parent field definition"""
        from jsonalchemy.errors import FieldParserException
        tmp_file_5 = tempfile.NamedTemporaryFile()
        config_5 = '''
        @extend
        wrong_field:
            """ Desc """
        '''
        tmp_file_5.write(config_5)
        tmp_file_5.flush()

        fields = list(self.metadata.fields)
        fields.append(tmp_file_5.name)
        self.metadata._cache_fields = fields
        self.assertRaises(
            FieldParserException, self.field_parser.reparse)
        tmp_file_5.close()

    def test_field_rules(self):
        """JsonAlchemy - field parser"""
        field_definitions = self.field_parser.field_definitions()
        assert len(field_definitions) >= 22
        # Check that all files are parsed
        assert 'authors' in field_definitions
        assert 'title' in field_definitions
        # Check work around for [n] and [0]
        assert field_definitions['doi']['pid']
        # Check if derived and calulated are well parserd
        self.assertTrue('dummy' in self.field_parser.field_definitions())
        assert self.field_parser.field_definitions()['dummy']['pid'] == 2
        assert (
            field_definitions['dummy']['rules'].keys() == ['json', 'derived']
        )
        assert len(field_definitions['dummy']['producer']) == 2
        assert self.field_parser.field_definitions()['_random']
        # Check override
        value = {'a': 'a', 'b': 'b', 'k': 'k'}  # noqa
        self.assertEquals(
            eval(self.field_parser.field_definitions()
                 ['title']['rules']['marc'][1]['function']),
            {'form': 'k', 'subtitle': 'b', 'title': 'a'})
        # Check extras
        self.assertTrue(
            'json_ext' in
            self.field_parser.field_definitions()['modification_date']
        )

        tmp = self.field_parser.field_definitions()
        self.field_parser.reparse()
        self.assertEquals(
            len(self.field_parser.field_definitions()), len(tmp))

    def test_field_hidden_decorator(self):
        """JsonAlchemy - field hidden decorator."""
        # Check that all files are parsed
        assert 'hidden_basic' in self.field_parser.field_definitions()
        # Check default hidden value
        assert not self.field_parser.field_definitions()['_id']['hidden']
        # Check hidden field
        assert self.field_parser.field_definitions()['hidden_basic']['hidden']

    def test_wrong_field_name_inside_model(self):
        """JSONAlchmey - wrong field name inside model"""
        from jsonalchemy.errors import ModelParserException
        tmp_file_8 = tempfile.NamedTemporaryFile()
        config_8 = '''
        fields:
            not_existing_field
        '''
        tmp_file_8.write(config_8)
        tmp_file_8.flush()
        self.metadata.models.append(tmp_file_8.name)
        self.assertRaises(
            ModelParserException, self.model_parser.reparse)
        tmp_file_8.close()

    def test_model_definitions(self):
        """JsonAlchemy - model parser"""
        self.assertTrue(len(self.model_parser.model_definitions) >= 2)
        self.assertTrue(
            'test_base' in self.model_parser.model_definitions)
        tmp = self.model_parser.model_definitions
        self.model_parser.reparse()
        self.assertEquals(
            len(self.model_parser.model_definitions), len(tmp))

    def test_resolve_several_models(self):
        """JSONAlchemy - test resolve several models"""
        test_model = self.model_parser.model_definitions['test_model']
        self.assertEquals(
            self.model_parser.resolve_models('test_model')['fields'],
            test_model['fields'])
        self.assertEquals(
            self.model_parser.resolve_models(
                ['test_base', 'test_model'])['fields'],
            test_model['fields'])

    def test_field_name_model_based(self):
        """JSONAlchemy - field name model based"""
        field_model_def = self.model_parser.field_definition_model_based(
            'title', 'test_model')
        field_def = self.field_parser.field_definitions()['title_title']

        value = {'a': 'Awesome title', 'b': 'sub title', 'k': 'form'}
        from jsonalchemy.utils import try_to_eval

        self.assertEqual(
            try_to_eval(field_model_def['rules'][
                        'marc'][0]['function'], value=value),
            try_to_eval(field_def['rules']['marc'][0]['function'],
                        value=value))

    def test_guess_legacy_field_names(self):
        """JsonAlchemy - check legacy field names"""
        self.assertEquals(
            guess_legacy_field_names(('100__a', '245'), 'marc', self.metadata),
            {'100__a': ['_first_author.full_name'], '245': ['title']})
        self.assertEquals(
            guess_legacy_field_names('foo', 'bar', self.metadata), {'foo': []})

    def test_get_producer_rules(self):
        """JsonAlchemy - check producer rules"""
        self.assertEquals(len(
            get_producer_rules('keywords', 'json_for_marc', self.metadata)
        ), 1)
        self.assertRaises(
            KeyError,
            lambda: get_producer_rules('foo', 'json_for_marc', self.metadata))
