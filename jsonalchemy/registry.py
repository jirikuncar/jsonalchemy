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

import os
import re
import six
import importlib
import pkgutil

from functools import partial
from pkg_resources import resource_listdir, resource_isdir

re_cfg = re.compile(r".*\.cfg$")


def generate_pkg_resources(pkg, module_name, re_filename=None):
    """Generate list of package resourses."""
    pkg_dirname = os.path.dirname(importlib.import_module(pkg).__file__)
    if resource_isdir(pkg, module_name):
        for filename in resource_listdir(pkg, module_name):
            if re_filename is None or re_filename.match(filename):
                yield os.path.join(pkg_dirname, module_name, filename)


def find_modules(import_path):
    """Iterate over submodules of given module."""
    module = importlib.import_module(import_path)
    basename = module.__name__ + '.'
    for importer, modname, ispkg in pkgutil.iter_modules(module.__path__):
        if not ispkg:
            yield basename + modname


class Package(object):

    """Load extensions from given package."""

    def __init__(self, package):
        if not isinstance(package, six.string_types):
            package = module.__path__
        self.package = package

    def _find(self, name):
        try:
            for mod in find_modules(self.package + '.' + name):
                try:
                    yield importlib.import_module(mod)
                except ImportError:
                    pass
        except ImportError:
            return

    @property
    def contexts(self):
        return dict((module.__name__.split('.')[-1], module.context)
                    for module in self._find('contexts')) or {}

    @property
    def parsers(self):
        return dict((m.parser.__parsername__, m.parser)
                    for m in self._find('parsers')) or {}

    @property
    def producers(self):
        return dict((m.__name__.split('.')[-1], m.produce)
                    for m in self._find('producers')) or {}

    @property
    def readers(self):
        return dict((m.__name__.split('.')[-1].split('_')[0], m.reader)
                    for m in self._find('readers')) or {}

    @property
    def functions(self):
        return dict((module.__name__.split('.')[-1],
                    getattr(module, module.__name__.split('.')[-1]))
                    for module in self._find('functions')) or {}

    @property
    def fields(self):
        return list(generate_pkg_resources(
            self.package, 'fields', re_filename=re_cfg) or [])

    @property
    def models(self):
        return list(generate_pkg_resources(
            self.package, 'models', re_filename=re_cfg) or [])


class MetaData(object):

    __default_package__ = 'jsonalchemy.jsonext'

    def __init__(self, packages=None):
        """Initialize metadata with a list of packages."""
        self.packages = map(Package, packages or [self.__default_package__])

    def _dict_merge(self, attr):
        value = getattr(self, '_cache_' + attr, None)
        if value is None:
            value = {}
            for package in self.packages:
                value.update(getattr(package, attr, {}))
            setattr(self, '_cache_' + attr, value)
        return value

    def _list_merge(self, attr):
        value = getattr(self, '_cache_' + attr, None)
        if value is None:
            value = []
            for package in self.packages:
                value += list(getattr(package, attr, []))
            setattr(self, '_cache_' + attr, value)
        return value

    @property
    def parsers(self):
        return self._dict_merge('parsers')

    @property
    def producers(self):
        return self._dict_merge('producers')

    @property
    def readers(self):
        return self._dict_merge('readers')

    @property
    def functions(self):
        return self._dict_merge('functions')

    @property
    def contexts(self):
        return self._dict_merge('contexts')

    @property
    def fields(self):
        return self._list_merge('fields')

    @property
    def models(self):
        return self._list_merge('models')

    def legacy_field_matchings(self):
        """Get all the legacy mappings for a given namespace.

        If the namespace does not exist, it tries to create it first

        :see: guess_legacy_field_names()
        """
        if getattr(self, '_legacy_field_matchings', None) is None:
            if getattr(self, 'field_parser', None) is None:
                from .parser import FieldParser
                self.field_parser = FieldParser(self)
            self.field_parser.field_definitions()
        return self._legacy_field_matchings

    def _filter_parser(self, attrname, parentcls):
        attr = getattr(self, attrname, None)
        if attr is None:
            attr = dict(
                (name, parser)
                for name, parser in six.iteritems(self.parsers)
                if issubclass(parser, parentcls))
            setattr(self, attrname, attr)
        return attr

    @property
    def field_extensions(self):
        """Get the field parser extensions from the parser registry."""
        from .parser import FieldBaseExtensionParser
        return self._filter_parser('_field_extensions',
                                   FieldBaseExtensionParser)

    @property
    def decorator_before_extensions(self):
        """TODO."""
        from .parser import DecoratorBeforeEvalBaseExtensionParser
        return self._filter_parser('_decorator_before_extensions',
                                   DecoratorBeforeEvalBaseExtensionParser)

    @property
    def decorator_on_extensions(self):
        """TODO."""
        from .parser import DecoratorOnEvalBaseExtensionParser
        return self._filter_parser('_decorator_on_extensions',
                                   DecoratorOnEvalBaseExtensionParser)

    @property
    def decorator_after_extensions(self):
        """TODO."""
        from .parser import DecoratorAfterEvalBaseExtensionParser
        return self._filter_parser('_decorator_after_extensions',
                                   DecoratorAfterEvalBaseExtensionParser)
