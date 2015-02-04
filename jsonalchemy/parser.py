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

"""Fields and models configuration loader.

This module uses `pyparsing <http://pyparsing.wikispaces.com/>`_ to read
from thedifferent configuration files the field and model definitions.

Default extensions to both parsers could be added inside
:mod:`jsonalchemy.jsonext.parsers`
"""
import os
import six

from pyparsing import ParseException, FollowedBy, Suppress, OneOrMore, Word, \
    LineEnd, ZeroOrMore, Optional, Literal, alphas, alphanums, \
    originalTextFor, nestedExpr, quotedString, removeQuotes, lineEnd, \
    empty, col, restOfLine, delimitedList, Each, Keyword, commaSeparatedList, \
    Group

from .errors import FieldParserException, ModelParserException

ParseException.defaultWhitespaceChars = (' \r\t')

COMMENT = (Literal("#") + restOfLine + LineEnd()).suppress()

IDENT = Word(alphanums + '_')
DICT_DEF = originalTextFor(nestedExpr('{', '}'))
LIST_DEF = originalTextFor(nestedExpr('[', ']'))
DICT_ACCESS = LIST_ACCESS = originalTextFor(IDENT + nestedExpr('[', ']'))

PYTHON_ALLOWED_EXPR = (DICT_DEF ^ LIST_DEF ^ DICT_ACCESS ^
                       LIST_ACCESS ^ restOfLine
                       ).setParseAction(lambda toks: toks[0])


def indentedBlock(expr, indent_stack, indent=True):
    """Define space-delimited indentation blocks.

    Helper method for defining space-delimited indentation blocks, such as
    those used to define block statements in Python source code.

    There is also a version in pyparsing but doesn't seem to be working fine
    with JSONAlchemy cfg files.
    """
    def check_sub_indent(string, location, tokens):
        """Check the indentation."""
        cur_col = col(location, string)
        if cur_col > indent_stack[-1]:
            indent_stack.append(cur_col)
        else:
            raise ParseException(string, location, "not a subentry")

    def check_unindent(string, location, tokens):
        """Check the 'undentation'."""
        if location >= len(string):
            return
        cur_col = col(location, string)
        if not(cur_col < indent_stack[-1] and cur_col <= indent_stack[-2]):
            raise ParseException(string, location, "not an unindent")

    def do_unindent():
        """Unindent."""
        indent_stack.pop()

    indent = lineEnd.suppress() + empty + empty.copy()\
        .setParseAction(check_sub_indent)
    undent = FollowedBy(empty).setParseAction(check_unindent)
    undent.setParseAction(do_unindent)

    return indent + expr + undent


def _create_field_parser(metadata):
    """Create a parser that can handle field definitions.

    BFN like grammar::

        rule       ::= [pid | extend | override]
                       json_id ["," aliases]":"
                           body
        json_id    ::= (letter|"_") (letter|digit|_)*
        aliases    ::= json_id ["," aliases]

        pid        ::= @persistent_identifier( level )
        extend     ::= @extend
        override   ::= @override
        hidden     ::= @hidden

        body       ::=(creator* | derived | calculated) (extensions)*

        creator    ::= [decorators] format "," tag "," expr
        derived    ::= [decorators] expr
        calculated ::= [decorators] expr

    To check the syntactics of the parser extensions or decorators please go to
    :mod:`jsonalchemy.jsonext.parsers`
    """
    indent_stack = [1]

    # Independent/special decorators
    persistent_identifier = (
        Keyword('@persistent_identifier').suppress() + nestedExpr()
    ).setResultsName('pid').setParseAction(lambda toks: int(toks[0][0]))
    override = Keyword('@override').suppress()\
        .setResultsName('override')\
        .setParseAction(lambda toks: True)
    extend = Keyword('@extend').suppress()\
        .setResultsName('extend')\
        .setParseAction(lambda toks: True)
    hidden = Keyword('@hidden').suppress()\
        .setResultsName('hidden')\
        .setParseAction(lambda toks: True)
    rule_decorators = (Optional(persistent_identifier) &
                       Optional(override) &
                       Optional(extend) &
                       Optional(hidden))

    # Field definition decorators
    field_decorators = Each(
        [Optional(parser.parse_element(indent_stack))
         for parser in six.itervalues(metadata.parsers)
         if issubclass(parser, DecoratorBaseExtensionParser)])

    # Creator rules
    creator_body = (
        Optional(field_decorators).setResultsName('decorators') +
        Word(alphas, alphanums + '_') +
        Literal(',').suppress() +
        quotedString.setParseAction(removeQuotes) +
        Literal(',').suppress() +
        PYTHON_ALLOWED_EXPR
    ).setParseAction(lambda toks: {
        'source_format': toks[-3],
        'source_tags': toks[-2].split(' '),
        'function': compile(toks[-1].strip(), '', 'eval'),
        'type': 'creator',
        'decorators': toks.decorators.asDict()}
    ).setResultsName('creator_def', listAllMatches=True)
    creator = (Keyword('creator:').suppress() +
               indentedBlock(OneOrMore(creator_body), indent_stack))

    # Derived and calculated rules
    der_calc_body = (Optional(field_decorators).setResultsName('decorators') +
                     PYTHON_ALLOWED_EXPR)
    derived = (
        Keyword('derived:').suppress() +
        indentedBlock(der_calc_body, indent_stack)
    ).setParseAction(lambda toks: {
        'source_format': 'derived',
        'source_tags': None,
        'function': compile(toks[-1].strip(), '', 'eval'),
        'type': 'derived',
        'decorators': toks.decorators.asDict()}).setResultsName('derived_def')
    calculated = (
        Keyword('calculated:').suppress() +
        indentedBlock(der_calc_body, indent_stack)
    ).setParseAction(lambda toks: {
        'source_format': 'calculated',
        'source_tags': None,
        'function': compile(toks[-1].strip(), '', 'eval'),
        'type': 'calculated',
        'decorators': toks.decorators.asDict()
    }).setResultsName('calculated_def')

    rule_sections = [Optional(creator | derived | calculated), ]
    rule_sections.extend([Optional(parser.parse_element(indent_stack))
                          for parser in six.itervalues(metadata.parsers)
                          if issubclass(parser, FieldBaseExtensionParser)])

    json_id = (IDENT +
               Optional(Suppress(',') +
                        delimitedList(Word(alphanums + '_'))) +
               Suppress(':')
               ).setResultsName('field')\
        .setParseAction(lambda toks: {'json_id': toks[0],
                                      'aliases': toks[1:]})

    rule = Group(Optional(rule_decorators) +
                 json_id +
                 indentedBlock(Each(rule_sections), indent_stack)
                 )

    return OneOrMore(COMMENT.suppress() | rule)


def _create_model_parser(metadata):
    """
    Create a parser that can handle model definitions.

    BFN like grammar::

        TODO

    Note: Unlike the field configuration files where you can specify more than
    one field inside each file for the models only one definition is
    allowed by file.
    """
    def build_dict_for_fields(tokens):
        """Build the dictionary wih the field definitions.

        E.g. ``{'field_name': 'json_identifier'}``
        """
        dict_ = dict()
        for token in tokens:
            if len(token) == 1:
                dict_[token[0]] = token[0]
            else:
                dict_[token[1]] = token[0]
        return dict_

    indent_stack = [1]

    field = Group(Word(alphanums + '_') +
                  Optional(Literal('=').suppress() + Word(alphanums + '_')))
    fields = (Keyword('fields:').suppress() +
              indentedBlock(ZeroOrMore(field), indent_stack)
              ).setParseAction(build_dict_for_fields).setResultsName('fields')

    bases = (Keyword('bases:').suppress() +
             indentedBlock(commaSeparatedList, indent_stack)
             ).setResultsName('bases')

    sections = [fields, Optional(bases), ]
    sections.extend([Optional(parser.parse_element(indent_stack))
                     for parser in six.itervalues(metadata.parsers)
                     if issubclass(parser, ModelBaseExtensionParser)])
    rules = Each(sections)

    return ZeroOrMore(COMMENT) & rules


class FieldParser(object):

    """Field definitions parser."""

    def __init__(self, metadata):
        """Initialize."""
        # Autodiscover cfg files
        self.metadata = metadata
        self.metadata.field_parser = self

        self._field_definitions = None
        """List of all the rules needed to create and validate json fields."""

    def field_extensions(self):
        """Get the field parser extensions from the parser registry."""
        return self.metadata.field_extensions

    def decorator_before_extensions(self):
        """TODO."""
        return self.metadata.decorator_before_extensions

    def decorator_on_extensions(self):
        """TODO."""
        return self.metadata.decorator_on_extensions

    def decorator_after_extensions(self):
        """TODO."""
        return self.metadata.decorator_after_extensions

    def field_definitions(self):
        """
        Get all the field definitions from a given namespace.

        If the namespace does not exist, it tries to create it first
        """
        if self._field_definitions is None:
            self._create()
        return self._field_definitions

    def reparse(self):
        self._create()

    def _create(self):
        """
        Create the fields and legacy fields definitions from configuration.

        Fills up _field_definitions dictionary with
        the rules defined inside the configuration files.

        This method should not be used (unless you really know what your are
        doing), use instead :meth:`reparse`
        """
        self._field_definitions = {}

        stand_by_rules = []

        parser = _create_field_parser(self.metadata)

        for field_file in self.metadata.fields:
            try:
                rules = parser.parseFile(field_file, parseAll=True)
            except ParseException as e:
                raise FieldParserException(
                    "Cannot parse file '%s',\n%s" % (field_file, str(e)))

            for rule in rules:
                if (rule.field['json_id'] in self._field_definitions)\
                        and not rule.extend and not rule.override:
                    raise FieldParserException(
                        "Name error: '%s' field is duplicated '%s'"
                        % (rule.field['json_id'], field_file))
                if (rule.field['json_id'] not in
                        self._field_definitions)\
                        and (rule.extend or rule.override):
                    stand_by_rules.append(rule)
                else:
                    self._create_rule(rule)

        for rule in stand_by_rules:
            if rule.field['json_id'] not in \
                    self._field_definitions:
                raise FieldParserException(
                    "Name error: '%s' field is not defined but is "
                    "marked as 'extend' or 'override'"
                    % (rule.field['json_id'], ))
            self._create_rule(rule)

    def _create_rule(self, rule):
        """
        Create the field and legacy definitions.

        The result looks like this.

        .. code-block:: json

            {key: { override: True/False,
                    extend: True/False,
                    hidden: True/False,
                    aliases: [],
                    pid: num/None,
                    rules: {'master_format_1': [{rule1}, {rule2}, ...],
                            'master_format_2': [....],
                             ......
                            'calculated': [....],
                            'derived': [...]}

                    .... extensions ....
                   }
            }

        Each of the rule (rule1, rule2, etc.) has the same content.

        .. code-block:: json

            {'source_format' : source_format/calculated/derived,
             'source_tag'    : source_tag/None,
             'function'      : python code to apply to the master value,
             'decorators'    : {}
            }

        """
        json_id = rule.field['json_id']

        # TODO: check if pyparsing can handle this!
        all_type_def = []
        if rule.creator_def:
            all_type_def.extend(rule.creator_def.asList())
        if rule.calculated_def:
            all_type_def.append(rule.calculated_def)
        elif rule.derived_def:
            all_type_def.append(rule.derived_def)

        rules = self._field_definitions[json_id]\
            .get('rules', {}) if rule.extend else dict()

        for field_def in all_type_def:
            self.__create_decorators_content(rule, field_def)
            if field_def['source_format'] not in rules:
                rules[field_def['source_format']] = list()
            rules[field_def['source_format']].append(field_def)

        if 'json' not in rules:
            rules['json'] = [{'source_format': 'json',
                              'source_tags': [json_id],
                              'function': compile('value', '', 'eval'),
                              'type': 'creator',
                              'decorators': {'before': {},
                                             'on': {},
                                             'after': {}
                                             }
                              }]

        rule_dict = dict()
        rule_dict['aliases'] = rule.field['aliases']
        rule_dict['pid'] = rule.pid if rule.pid is not '' else None
        rule_dict['override'] = rule.override if rule.override else False
        rule_dict['extend'] = rule.extend if rule.extend else False
        rule_dict['hidden'] = rule.hidden if rule.hidden else False
        rule_dict['rules'] = rules

        if rule.override:
            self._field_definitions[json_id]\
                .update(rule_dict)
        elif rule.extend:
            self._field_definitions[json_id][
                'aliases'].extend(rule_dict['aliases'])
            self._field_definitions[json_id][
                'hidden'] |= rule_dict['hidden']
            self._field_definitions[json_id][
                'extend'] = True
        else:
            self._field_definitions[json_id] = \
                rule_dict

        self.__resolve_parser_extensions(rule)

    def __resolve_parser_extensions(self, rule):
        """
        Apply the incoming rule for each extension.

        For each of the extension available it tries to apply it in the
        incoming rule
        """
        json_id = rule.field['json_id']
        for name, parser in six.iteritems(self.field_extensions()):
            if getattr(rule, name, None):
                self._field_definitions[json_id][name] = parser.create_element(
                    rule, self.metadata)

    def __create_decorators_content(self, rule, field_def):
        """Extract from the rule all the possible decorators."""
        decorators = {'before': {}, 'on': {}, 'after': {}}

        for name, parser in six.iteritems(
                self.decorator_before_extensions()):
            if name in field_def['decorators']:
                decorators['before'][name] = \
                    parser.create_element(rule, field_def,
                                          field_def['decorators'][name],
                                          self.metadata)
        for name, parser in six.iteritems(
                self.decorator_on_extensions()):
            if name in field_def['decorators']:
                decorators['on'][name] = \
                    parser.create_element(rule, field_def,
                                          field_def['decorators'][name],
                                          self.metadata)

        for name, parser in six.iteritems(
                self.decorator_after_extensions()):
            if name in field_def['decorators']:
                decorators['after'][name] = \
                    parser.create_element(rule, field_def,
                                          field_def['decorators'][name],
                                          self)

        field_def['decorators'] = decorators


class ModelParser(object):

    """Record model parser."""

    def __init__(self, metadata):
        """Initialize the model parser with the given namespace."""
        self.metadata = metadata
        self.field_parser = FieldParser(metadata)

        self._model_definitions = None
        """Contain all the model definitions order by namespace."""

        self._parser_extensions = None
        """Model only parser extensions."""

    def parser_extensions(self):
        """Get only the model parser extensions from the parser registry."""
        if self._parser_extensions is None:
            self._parser_extensions = dict(
                (name, parser) for name, parser in
                six.iteritems(self.metadata.parsers)
                if issubclass(parser, ModelBaseExtensionParser))
        return self._parser_extensions

    @property
    def model_definitions(self):
        """
        Get all the model definitions given a namespace.

        If the namespace does not exist, it tries to create it first.
        """
        if self._model_definitions is None:
            self._create()
        return self._model_definitions

    def field_definition_model_based(self, field_name, model_name):
        """
        Get the real field definition based on the model name.

        Based on a model name (and namespace) it gets the real field
        definition.
        """
        model_index = ','.join(model_name) if isinstance(model_name, list) \
            else model_name

        if getattr(self, '_resolve_models', None) is None:
            self._resolve_models = {}

        if getattr(self, '_resolve_models_field', None) is None:
            self._resolve_models_field = {}

        new_model = self._resolve_models.get(
            model_index,
            self.resolve_models(model_name)
        )
        self._resolve_models[model_index] = new_model
        self._resolve_models_field.setdefault(model_index, {})

        json_id = self._resolve_models_field.get(model_index, {}).get(
            field_name, None)

        if json_id is None:
            json_id = field_name
            for j, f in six.iteritems(new_model['fields']):
                if f == field_name:
                    json_id = j
                    break
            self._resolve_models_field[model_index][field_name] = json_id

        return self.field_parser.field_definitions().get(json_id, None)

    def resolve_models(self, model_list):
        """Resolve all the field conflicts.

        From a given list of model definitions resolves all the field conflicts
        and returns a new model definition containing all the information from
        the model list.
        The field definitions are resolved from left-to-right.

        :param model_list: It could be also a string, in which case the model
            definition is returned as it is.
        :return: Dictionary containing the union of the model definitions.
        """
        if model_list == '__default__':
            keys = self.field_parser.field_definitions().keys()
            return {
                'fields': dict((key, key) for key in keys),
                'bases': [],
            }

        if isinstance(model_list, six.string_types):
            try:
                return self.model_definitions[model_list]
            except KeyError:
                keys = self.field_parser.field_definitions().keys()
                return {
                    'fields': dict((key, key) for key in keys),
                    'bases': [],
                }

        new_model = {'fields': dict(), 'bases': list()}
        for model in model_list:
            if model == '__default__' or model not in self.model_definitions:
                keys = self.field_parser.field_definitions().keys()
                new_model['fields'].update(dict((key, key) for key in keys))
            else:
                model_def = self.model_definitions.get(model, {})
                new_model['fields'].update(model_def.get('fields', {}))
                new_model['bases'].extend(model_def.get('bases', []))
                for key, value in six.iteritems(model_def):
                    if key in ('fields', 'bases'):
                        continue
                    new_model[key] = self.parser_extensions()[key]\
                        .extend_model(new_model.get(key), value)

        return new_model

    def reparse(self):
        self.field_parser._create()
        self._create()

    def _create(self):
        """Fill up _model_definitions dictionary.

        It uses what is written inside the `*.cfg`  model descriptions

        It also resolve inheritance at creation time and name matching for the
        field names present inside the model file

        The result looks like this:

        .. code-block:: json

            {'model': {'fields': {'name_for_fieldfield1': json_id1,
                                  'name_for_field2': json_id2,
                                            ....
                                  'name_for_fieldN': fieldN },
                       'bases: [(inherit_from_list), ...]
                       },
             ...
            }

        This method should not be used (unless you really know what your are
        doing).

        :raises: ModelParserException in case of missing model definition
                 (helpful if we use inheritance) or in case of unknown field
                 name.
        """
        self._model_definitions = {}

        parser = _create_model_parser(self.metadata)
        for model_file in self.metadata.models:
            model_name = os.path.basename(model_file).split('.')[0]
            if model_name in self._model_definitions:
                raise ModelParserException(
                    "Already defined model: %s" % (model_name,))

            self._model_definitions[model_name] = {
                'fields': {},
                'bases': [],
            }

            try:
                model_definition = parser.parseFile(model_file, parseAll=True)
            except ParseException as e:
                raise ModelParserException(
                    "Cannot parse file %s,\n%s" % (model_file, str(e)))

            if not model_definition.fields:
                raise ModelParserException("Field definition needed")

            if any([json_id not in self.field_parser.field_definitions()
                    for json_id in model_definition.fields.values()]):
                raise ModelParserException(
                    "At least one field is no find in the field "
                    "definitions for file '%s'" % (model_file))
            self._model_definitions[model_name][
                'fields'] = model_definition.fields
            self._model_definitions[model_name][
                'bases'] = model_definition.bases.asList() \
                if model_definition.bases else []

            self.__resolve_parser_extensions(model_name, model_definition)

        self.__resolve_inheritance()

    def __resolve_inheritance(self):
        """Resolve the inheritance."""
        def resolve_ext_inheritance(ext_name, model_definition):
            for inherit_from in model_definition['bases']:
                base_model = self.model_definitions[inherit_from]
                model_definition[ext_name] = \
                    self.parser_extensions()[ext_name].inherit_model(
                        model_definition.get(ext_name),
                        resolve_ext_inheritance(ext_name, base_model))
            return model_definition.get(ext_name)

        def resolve_field_inheritance(model_definition):
            fields = {}
            for inherit_from in model_definition['bases']:
                base_model = self.model_definitions[inherit_from]
                fields.update(resolve_field_inheritance(base_model))
            if fields:
                inverted_fields = dict((v, k)
                                       for k, v in six.iteritems(fields))
                inverted_model_fields = dict((v, k) for k, v in six.iteritems(
                    model_definition['fields']))
                inverted_fields.update(inverted_model_fields)
                fields = dict((v, k)
                              for k, v in six.iteritems(inverted_fields))
            else:
                fields.update(model_definition['fields'])
            return fields

        for model_definition in self.model_definitions.values():
            model_definition['fields'] = resolve_field_inheritance(
                model_definition)
            for name, model_ext in \
                    six.iteritems(self.parser_extensions()):
                model_definition[name] = resolve_ext_inheritance(
                    name, model_definition)

    def __resolve_parser_extensions(self, model_name, model_def):
        """Apply the incoming rule for each available extension."""
        for name, parser in six.iteritems(self.parser_extensions()):
            if name in model_def:
                self._model_definitions[model_name][name] = \
                    parser.create_element(model_def, self.metadata)


def guess_legacy_field_names(fields, master_format, metadata):
    """Find the equivalent JSON field for the legacy field(s).

    Using the legacy rules written in the config file (@legacy) tries to find
    the equivalent json field for one or more legacy fields.

    .. doctest::

        >>> guess_legacy_fields(('100__a', '245'), 'marc', 'recordext')
        {'100__a':['authors[0].full_name'], '245':['title']}

    """
    res = {}
    if isinstance(fields, six.string_types):
        fields = (fields, )
    for field in fields:
        try:
            res[field] = metadata.legacy_field_matchings()[master_format].get(
                field, [])
        except (KeyError, TypeError):
            res[field] = []
    return res


def get_producer_rules(field, code, metadata, model=['__default__']):
    """Get all the producer rules related with the field and code.

    From the field definitions gets all the producer rules related with the
    field and the code (using also the namespace).

    For each producer rule the first element are the 'preconditions' to apply
    the rules and the second one are the actual rules.

    .. doctest::

        >>> from jsonalchemy.registry import MetaData
        >>> metadata = MetaData()
        >>> get_producer_rules('_first_author', 'json_for_marc', metadata)
        [((),
          {'100__a': 'full_name',
           '100__e': 'relator_name',
           '100__h': 'CCID',
           '100__i': 'INSPIRE_number',
           '100__u': 'affiliation'})]
        >>> get_producer_rules('title', 'json_for_marc', 'recordext')
        [[((), {'245__a': 'title', '245__b': 'subtitle', '245__k': 'form'})]

    """
    if getattr(metadata, 'model_parser', None) is None:
        metadata.model_parser = ModelParser(metadata)

    try:
        return metadata.model_parser.field_definition_model_based(
            field, model).get('producer', {}).get(code, [])
    except AttributeError:
        raise KeyError(field)


class BaseExtensionParser(type):  # pylint: disable=E501,R0921

    """Metaclass for the configuration file extensions."""

    def __new__(mcs, name, bases, dict_):
        """TODO."""
        if not dict_.get('__parsername__'):
            dict_['__parsername__'] = name.lower().replace('parser', '')

        return super(BaseExtensionParser, mcs).__new__(mcs, name, bases, dict_)

    @classmethod
    def parse_element(mcs, indent_stack):
        """
        Parse the element.

        Using pyparsing defines a piece of the grammar to parse the
        extension from configuration file

        :return: pyparsing ParseElement
        """
        raise NotImplementedError()

    @classmethod
    def create_element(mcs, *args, **kwargs):
        """
        Create the element.

        Once the extension is parsed defines the actions that have to be taken
        to store inside the field_definitions the information needed or useful.
        """
        raise NotImplementedError()

    @classmethod
    def add_info_to_field(mcs, *args, **kwargs):
        """
        Define with information goes into the meta-metadata dictionary.

        Defines which information goes inside the ``__meta_metadata__``
        dictionary and how.
        """
        raise NotImplementedError()

    @classmethod
    def evaluate(mcs, *args, **kwargs):
        """
        Evaluate the field.

        Once the extension information is added to the field, whenever it gets
        accessed or modify this method is call for each of the extension set
        in the metadata of this field.
        """
        raise NotImplementedError()


class FieldBaseExtensionParser(six.with_metaclass(BaseExtensionParser)):

    """Base class for field parser extensions."""

    @classmethod
    def add_info_to_field(cls, json_id, info):
        """
        Create the content of ``extension_name``.

        Should create the content of ``__meta_metadata__.json.extension_name``
        """
        raise NotImplementedError()

    @classmethod
    def evaluate(cls, json, field_name, action, args):
        """
        Evaluate the field.

        Depending on the extension perform the actions that it defines using
        the current value as parameter. (It could cause side effects on the
        current json)
        """
        raise NotImplementedError()


class ModelBaseExtensionParser(six.with_metaclass(BaseExtensionParser)):

    """Base class for model parser extensions."""

    @classmethod
    def inherit_model(cls, current_value, base_value):
        """
        Inherit the model from other.

        When a model inherits from other (or several) it should resolve the
        inheritance taking the current value and the base value from the
        extension.
        """
        raise NotImplementedError()

    @classmethod
    def extend_model(cls, current_value, new_value):
        """
        Extend the model.

        When a json object is using several models this method should provide
        the logic to extend the content of the extensions.

        :return: the content of model[extension]
        """
        raise NotImplementedError()

    @classmethod
    def add_info_to_field(cls, info):
        """
        Define with information goes into the model dictionary.

        Defines which information goes inside the
        ``__meta_metadata__.__model__``  dictionary and how.

        """
        raise NotImplementedError()

    @classmethod
    def evaluate(cls, obj, args):
        """
        Get and modify the current object.

        Gets the current object (typically a SmartJson object) and modifies it
        accordingly with the extension nature.
        """
        raise NotImplementedError()


class DecoratorBaseExtensionParser(six.with_metaclass(BaseExtensionParser)):

    """Base class for decorator parser extension."""

    pass


class DecoratorBeforeEvalBaseExtensionParser(DecoratorBaseExtensionParser):

    """
    Base class for decorator parser extensions.

    This ones will be evaluated *before* any operation on the value.
    """

    @classmethod
    def evaluate(cls, reader, args):
        """Evaluate ``args`` and returns a boolean depending on them."""
        raise NotImplementedError()


class DecoratorOnEvalBaseExtensionParser(DecoratorBaseExtensionParser):

    """
    Base class for decorator parser extensions.

    this ones will be evaluated *while* the rule gets evaluated with the input
    value. (Therefore they have access to ``value``) This decorators are only
    useful for ``creator`` definitions.
    """

    @classmethod
    def evaluate(cls, value, metadata, args):
        """
        Evaluate ``args`` with the master value from the input.

        :returns: a boolean depending on them.
        """
        raise NotImplementedError()


class DecoratorAfterEvalBaseExtensionParser(DecoratorBaseExtensionParser):

    """
    Base class for decorator parser extensions.

    This one will be evaluated *after* the rule gets evaluated and before
    setting the value to the json.
    """

    @classmethod
    def add_info_to_field(cls, json_id, info, args):
        """
        Add a field to the JSON so it can be evaluated.

        When adding a new field to the json, if its definition uses the current
        decorator it adds the needed content in a way that ``evaluate`` can
        use.
        """
        raise NotImplementedError()

    @classmethod
    def evaluate(cls, json, field_name, action, args):
        """
        Evaluate the actions depending on the decoratior.

        Depending on the decorator performs the actions that it defines using
        the current value as parameter. (It could cause side effects on the
        current json).
        """
        raise NotImplementedError()
