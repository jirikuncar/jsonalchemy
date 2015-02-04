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

"""JSONAlchemy wrappers."""

import copy
import re
import six

from collections import MutableMapping
from six import iteritems

from .parser import ModelParser
from .reader import Reader


class SmartDict(object):

    """This dictionary allows to do some 'smart queries' to its content.

    Example:

    .. code-block:: python

        >>> d = SmartDict()
        >>> d['foo'] = {'a': 'world', 'b':'hello'}
        >>> d['a'] = [ {'b':1}, {'b':2}, {'b':3} ]
        >>> d['a']
        [ {'b':1}, {'b':2}, {'b':3} ]
        >>> d['a[0]']
        {'b':1}
        >>> d['a.b']
        [1,2,3]
        >>> d['a[1:]']
        [{'b':2}, {'b':3}]

    .. note::
        You can't use the reserved words '.', '[', ']' like a key.

        .. code-block:: python

            >>> d['.']
            >>> d[']']
            >>> d['.a']

        It is also not recommended initialize `SmartDict` with keys from
        within the list of reserved words.

        .. code-block:: python

            >>> d = SmartDict({'a': 3, 'b': {'.': 5}})
    """

    split_key_pattern = re.compile('\.|\[')
    main_key_pattern = re.compile('\..*|\[.*')

    def __init__(self, d=None):
        self._dict = d if d is not None else dict()

    def __getitem__(self, key):
        """Return item as `dict.__getitem__` but using 'smart queries'.

        .. note::
            Accessing one value in a normal way, meaning d['a'], is almost as
            fast as accessing a regular dictionary. But using the special
            name convention is a bit slower than using the regular access:

            .. code-block:: python

                >>> %timeit x = dd['a[0].b']
                100000 loops, best of 3: 3.94 us per loop
                >>> %timeit x = dd['a'][0]['b']
                1000000 loops, best of 3: 598 ns per loop
        """
        def getitem(k, v):
            if isinstance(v, dict):
                return v[k]
            elif ']' in k:
                k = k[:-1].replace('n', '-1')
                # Work around for list indexes and slices
                try:
                    return v[int(k)]
                except ValueError:
                    return v[slice(*map(
                        lambda x: int(x.strip()) if x.strip() else None,
                        k.split(':')
                    ))]
            else:
                tmp = []
                for inner_v in v:
                    tmp.append(getitem(k, inner_v))
                return tmp

        # Check if we are using python regular keys
        try:
            return self._dict[key]
        except KeyError:
            pass

        keys = SmartDict.split_key_pattern.split(key)
        value = self._dict
        for k in keys:
            value = getitem(k, value)
        return value

    def __setitem__(self, key, value, extend=False, **kwargs):
        # check if the key is composed only by special chars
        if key[0] in ['.', ']', '[']:
            # this kind of key is not supported!
            raise KeyError

        if '.' not in key and ']' not in key and not extend:
            self._dict[key] = value
        else:
            keys = SmartDict.split_key_pattern.split(key)
            self.__setitem(self._dict, keys[0], keys[1:], value, extend)

    def __delitem__(self, key):
        """Delete item only from first level dictionary keys."""
        del self._dict[key]

    def __contains__(self, key):

        if '.' not in key and '[' not in key:
            return key in self._dict
        try:
            self[key]
        except:
            return False
        return True

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self._dict == other._dict)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def keys(self):
        return self._dict.keys()

    def items(self):
        return self._dict.items()

    def iteritems(self):
        """Proxy to `dict.iteritems`."""
        return iteritems(self._dict)

    def iterkeys(self):
        """Proxy to `dict.iterkeys`."""
        return self._dict.iterkeys()

    def itervalues(self):
        """Proxy to `dict.itervalues`."""
        return self._dict.itervalues()

    def has_key(self, key):
        """Return ``True`` if ``key`` is in dictionary."""
        return key in self

    def __repr__(self):
        """Proxy to `dict.__repr__`."""
        return repr(self._dict)

    def __setitem(self, chunk, key, keys, value, extend=False):
        """Helper function to fill up the dictionary."""
        def setitem(chunk):
            if keys:
                return self.__setitem(chunk, keys[0], keys[1:], value, extend)
            else:
                return value

        if key in ['.', ']']:
            chunk[key] = value
        elif ']' in key:  # list
            key = int(key[:-1].replace('n', '-1'))
            if extend:
                if chunk is None:
                    chunk = [None, ]
                else:
                    if not isinstance(chunk, list):
                        chunk = [chunk, ]
                    if key != -1:
                        chunk.insert(key, None)
                    else:
                        chunk.append(None)
            else:
                if chunk is None:
                    chunk = [None, ]
            chunk[key] = setitem(chunk[key])
        else:  # dict
            if extend:
                if chunk is None:
                    chunk = {}
                    chunk[key] = None
                    chunk[key] = setitem(chunk[key])
                elif key not in chunk:
                    chunk[key] = None
                    chunk[key] = setitem(chunk[key])
                else:
                    if keys:
                        chunk[key] = setitem(chunk[key])
                    else:
                        if not isinstance(chunk[key], list):
                            chunk[key] = [chunk[key], ]
                        chunk[key].append(None)
                        chunk[key][-1] = setitem(chunk[key][-1])
            else:
                if chunk is None:
                    chunk = {}
                if key not in chunk:
                    chunk[key] = None
                chunk[key] = setitem(chunk[key])

        return chunk

    def get(self, key, default=None):
        """Return value for given ``key`` or ``default`` value."""
        try:
            return self[key]
        except KeyError:
            return default

    def set(self, key, value, extend=False, **kwargs):
        """Extended standard set function."""
        self.__setitem__(key, value, extend, **kwargs)

    def update(self, E, **F):
        """Proxy `dict` update method."""
        self._dict.update(E, **F)

MutableMapping.register(SmartDict)


class DotableDict(dict):

    """Make nested python dictionaries accessable using dot notation.

    Example:

    .. code-block:: python

        >>> dotable = DotableDict({'a': [{'b': 3, 'c': 5}]})
        >>> dotable.a
        ...  [{'b': 3, 'c': 5}]
    """

    def __getattr__(self, key):
        """Return value from dictionary.

        .. todo:: allow ``dotable.a[0].b``
        """
        return self[key]

    def __setattr__(self, key, value):
        """Set value for given key in dictionary."""
        self[key] = value


class SmartJson(SmartDict):

    """Base class for Json structures."""

    def __init__(self, json=None, set_default_values=False,
                 process_model_info=False, metadata=None, **kwargs):
        """If no JSON, a new structure will be created.

        Typically the JSON structure needs a few mandatory fields and subfields
        that are created here, the final JSON should look like this::

            {
                '__meta_metadata__': {
                    '__additional_info__': {...},
                    '__model_info__': {'model_names': [...], ....},
                    '__aliases__': {...},
                    '__errors__': [...],
                    '__continuable_errors__': []
              }
            }

        The content of `__additional_info__` is, usually, the content of
        kwargs.

        This object maintains two different dictionaries, one with the pure
        JSON representation, `_dict` and a second one with the BSON
        representation of the former. This behavior helps whenever dealing with
        JSON databases as MongoDB or PostgreSQL.

        The content of the BSON dictionary is typically the same as in the JSON
        one, only if the `json` section is described in the definition of the
        field the content might change, a good example of this behavior are the
        date fields.
        See :class:`~.jsonext.parsers.json_extra_parser:JsonExtraParser`.

        :param json: JSON to build the dictionary.
        :param set_defaul_values: If `True` default values will be set.
        :param process_model_info: If `True` all model info will be parsed.
        :param kwargs: Everything that would be useful inside
            `__additional_info__`. Although it could be used also for:
            * `model=['model1', 'model2']`, in this case this key will be
            deleted from `kwargs` and used as model names inside
            `__model_info__`.
        """
        super(SmartJson, self).__init__(json)
        self._dict_bson = SmartDict()
        self._metadata = metadata

        if not json or '__meta_metadata__' not in json:
            model_names = kwargs.get('model', ['__default__', ])
            if 'model' in kwargs:
                del kwargs['model']
            if isinstance(model_names, six.string_types):
                model_names = [model_names, ]
            self._dict['__meta_metadata__'] = dict()
            self._dict['__meta_metadata__']['__additional_info__'] = kwargs
            self._dict['__meta_metadata__']['__model_info__'] = \
                dict(names=model_names)
            self._dict['__meta_metadata__']['__aliases__'] = dict()
            self._dict['__meta_metadata__']['__errors__'] = list()
            self._dict['__meta_metadata__']['__continuable_errors__'] = list()

        if process_model_info:
            self.metadata.reader.process_model_info(self)

        if set_default_values:
            self.set_default_values()

    @property
    def metadata(self):
        if self._metadata is None:
            raise RuntimeError("SmartJSON has no binded metadata.")
        return self._metadata

    def bind(self, metadata):
        self._metadata = metadata

    @property
    def reader(self):
        if getattr(self, '_reader', None) is None:
            cls = self.metadata.readers[self.additional_info['master_format']]
            self._reader = cls(self, blob=self._dict_bson,
                               metadata=self.metadata)
        return self._reader

    @property
    def additional_info(self):
        """Shortcut to `__meta_metadata__.__additional_info__`."""
        return DotableDict(self['__meta_metadata__']['__additional_info__'])

    @property
    def errors(self):
        """Shortcut to `__meta_metadata__.__errors__`."""
        return self._dict['__meta_metadata__']['__errors__']

    @property
    def continuable_errors(self):
        """Shortcut to `__meta_metadata__.__continuable_errors__`."""
        return self._dict['__meta_metadata__']['__continuable_errors__']

    @property
    def meta_metadata(self):
        """Shortcut to `__meta_metadata__`."""
        return DotableDict(self._dict['__meta_metadata__'])

    @property
    def model_info(self):
        """Shortcut to `__meta_metadata__.__model_info__`."""
        return DotableDict(self._dict['__meta_metadata__']['__model_info__'])

    def __getitem__(self, key, reset=False, **kwargs):
        """Like in `dict.__getitem__`.

        First it tries to load the value from the value from the BSON object,
        if it fails, or reset is set to `True`, looks into the JSON object for
        the `key`, applies all the extensions and decorators and return the
        value that is stored in the BSON object as a cached version.

        If the key is not found inside the dictionary, it tries before raising
        `KeyError` to figure out if it is dealing with an alias.

        :param key:
        :param reset: If the key corresponds to a field calculated on the fly
            the value will be calculated again.
        :param kwargs: Typically used to set:
            * `action`, Whether we are performing a `set` or a `get`.
            *`exclude`, from the list of extensions and decorators excludes the
            ones that are not required.

        :return: Like in `dict.__getitem__`
        """
        try:
            value = self._dict_bson[key]
            if value and not reset:
                return value
        except KeyError:
            # Try to find the key inside the json dict and load it
            pass
        main_key = SmartDict.main_key_pattern.sub('', key)
        if main_key == '__meta_metadata__':
            return super(SmartJson, self).__getitem__(key)
        elif main_key in self._dict:
            if main_key not in self.meta_metadata:
                self.reader.set(main_key)
            action = kwargs.get('action', 'get')
            exclude = kwargs.get('exclude', [])
            if 'extensions' not in exclude:
                for ext, args in \
                        six.iteritems(self.meta_metadata[main_key]['ext']):
                    if ext in exclude:
                        continue
                    self.metadata.field_extensions[ext].evaluate(
                        self, main_key, action, args)
            if 'decorators' not in exclude:
                for ext, args in \
                        six.iteritems(self.meta_metadata[main_key]['after']):
                    if ext in exclude:
                        continue
                    self.metadata.decorator_after_extensions[ext].evaluate(
                        self, main_key, action, args)

            return self._dict_bson[key]
        else:
            try:
                rest_of_key = SmartDict.main_key_pattern.findall(key)[0]
            except IndexError:
                rest_of_key = ''
            return self[
                self._dict['__meta_metadata__']['__aliases__'][main_key]
                + rest_of_key]

    def __setitem__(self, key, value, extend=False, **kwargs):
        """Like in `dict.__setitem__`.

        There are two possible scenarios, i) the key is already present in the
        dictionary (also its metadata), therefore a simple set in the first
        step, ii) or the key is not inside the dictionary, in this case the
        metadata for the field is fetched before performing the rest of the
        actions.

        Like in `__getitem__` after setting the value to the BSON dictionary
        the decorators and the extensions are evaluated and, if needed, the
        JSON representation of `value` is set into the JSON dictionary.

        :param key:
        :param value:
        :param extend: If `False` it behaves as `ditc.__setitem__`, if `True`
            creates a list with the previous content and append `value` to it.
        :param kwargs:Typically used to set:
            * `action`, Whether we are performing a `set` or a `get`.
            *`exclude`, from the list of extensions and decorators excludes the
            ones that are not required.
        """
        main_key = SmartDict.main_key_pattern.sub('', key)
        # If we have meta_metadata for the main key go ahead
        if main_key in self.meta_metadata:
            self._dict_bson.__setitem__(key, value, extend)
        # Othewise we need the meta_metadata
        else:
            self.reader.set(main_key)
            self._dict_bson.__setitem__(key, value, extend, **kwargs)
        action = kwargs.get('action', 'set')
        exclude = kwargs.get('exclude', [])
        if 'decorators' not in exclude:
            for ext, args in \
                    six.iteritems(self.meta_metadata[main_key]['after']):
                if ext in exclude:
                    continue
                self.metadata.decorator_after_extensions[ext].evaluate(
                    self, main_key, action, args)
        if 'extensions' not in exclude:
            for ext, args in \
                    six.iteritems(self.meta_metadata[main_key]['ext']):
                if ext in exclude:
                    continue
                self.metadata.field_extensions[ext].evaluate(
                    self, main_key, action, args)

    def __str__(self):
        """Representation of the object **without** the meta_metadata."""
        return self.dumps(without_meta_metadata=True).__str__()

    def __repr__(self):
        """Full string representation of the JSON object."""
        return self._dict.__repr__()

    def __delitem__(self, key):
        """Delete on key from the dictionary and its meta_metadata.

        Note: It only works with default python keys
        """
        self._dict.__delitem__(key)
        del self._dict['__meta_metadata__'][key]
        try:
            del self._dict_bson[key]
        except KeyError:
            pass

    def get(self, key, default=None, reset=False, **kwargs):
        """Like in `dict.get`."""
        try:
            return self.__getitem__(key, reset, **kwargs)
        except (KeyError, IndexError):
            return default

    def items(self, without_meta_metadata=False):
        """Like in `dict.items`."""
        for key in self.keys():
            if key == '__meta_metadata__' and without_meta_metadata:
                continue
            yield (key, self[key])
    iteritems = items

    def keys(self, without_meta_metadata=False):
        """Like in `dict.keys`."""
        for key in super(SmartJson, self).keys():
            if key == '__meta_metadata__' and without_meta_metadata:
                continue
            yield key

    def get_blob(self, *args, **kwargs):
        """To be override in the specific class.

        Should look for the original version of the file where the json came
        from.
        """
        raise NotImplementedError()

    def dumps(self, without_meta_metadata=False, with_calculated_fields=False,
              clean=False, keywords=None, filter_hidden=False):
        """Create the JSON friendly representation of the current object.

        :param without_meta_metadata: by default ``False``, if set to ``True``
            all the ``__meta_metadata__`` will be removed from the output.
        :param wit_calculated_fields: by default the calculated fields are not
            dump, if they are needed in the output set it to ``True``
        :param clean: if set to ``True`` all the keys stating with ``_`` will
            be removed from the ouput
        :param keywords: list of keywords to dump. if None, return all

        :return: JSON friendly object
        """
        dict_ = copy.copy(self._dict)
        filter_keywords = keywords is not None and any(keywords)

        if without_meta_metadata:
            del dict_['__meta_metadata__']

        # skip the dict iteration
        if not any([clean, filter_keywords, filter_hidden,
                    with_calculated_fields]):
            return dict_

        for key, value in six.iteritems(self._dict):
            if (clean and key.startswith('_')) or (
                    filter_keywords and key not in keywords) or (
                    filter_hidden and self.meta_metadata.get(key, {}).get(
                        'hidden', False)):
                del dict_[key]
                continue

            if with_calculated_fields:
                if value is None and \
                        self.meta_metadata[key]['type'] == 'calculated':
                    dict_[key] = self[key]

        return dict_

    def loads(self, without_meta_metadata=False, with_calculated_fields=True,
              clean=False):
        """Create the BSON representation of the current object.

        :param without_meta_metadata: if set to ``True`` all the
            ``__meta_metadata__`` will be removed from the output.
        :param wit_calculated_fields: by default the calculated fields are in
            the output, if they are not needed set it to ``False``
        :param clean: if set to ``True`` all the keys stating with ``_`` will
            be removed from the ouput

        :return: JSON friendly object

        """
        dict_ = dict()
        for key in self.keys():
            dict_[key] = self[key]

        if without_meta_metadata:
            del dict_['__meta_metadata__']
        if not with_calculated_fields:
            for key in self.keys():
                if self.meta_metadata[key]['type'] == 'calculated':
                    del dict_[key]
        if clean:
            for key in list(dict_.keys()):
                if key.startswith('_'):
                    del dict_[key]

        return dict_

    def produce(self, producer_code, fields=None):
        """Create a different flavor of `JSON` depending on `procuder_code`.

        :param producer_code: One of the possible producers listed in the
            `producer` section inside the field definitions.
        :param fields: List of fields that should be present in the output, if
            `None` all fields from `self` will be used.

        :return: It depends on each producer, see producer folder inside
            `jsonext`, typically `dict`.
        """
        return self.metadata.producers[producer_code](self, fields=fields)

    def set_default_values(self, fields=None):
        """Set default value for the fields using the schema definition.

        :param fields: List of fields to set the default value, if `None` all.

        """
        raise NotImplementedError('Missing implementation in this version')

    def validate(self, validator=None):
        """Validate using current JSON content using Cerberus.

        See: (Cerberus)[http://cerberus.readthedocs.org/en/latest].

        :param validator: Validator to be used, if `None`
            :class:`~.validator.Validator`
        """
        if validator is None:
            from .validator import Validator as validator
        schema = dict()
        model_fields = ModelParser.resolve_models(
            self.model_info.names,
            self.additional_info.namespace).get('fields', {})
        for field in self.keys():
            if not field == '__meta_metadata__' and \
                    field not in model_fields and \
                    self.meta_metadata[field]['json_id'] not in model_fields:
                model_fields[field] = self.meta_metadata[field]['json_id']
        for json_id in model_fields.keys():
            try:
                schema.update(self.metadata.field_definitions[json_id].get(
                    'schema', {}))
            except (TypeError, KeyError):
                pass
        _validator = validator(schema=schema)
        _validator.validate(self)
        return _validator.errors


class SmartJsonLD(SmartJson):

    """Utility class for JSON-LD serialization."""

    def translate(self, context_name, context):
        """Translate object to fit given JSON-LD context.

        Should not inject context as this will be done at publication time.
        """
        raise NotImplementedError('Translation not required')

    def get_context(self, context):
        """Return the context definition identified by the parameter.

        If the context is not found in the current namespace, the received
        parameter is returned as is, the assumption being that a IRI was
        passed.

        :param context: context identifier
        """
        return self.metadata.contexts.get(context, context)

    def get_jsonld(self, context, new_context={}, format="full"):
        """Return the JSON-LD serialization.

        :param: context the context to use for raw publishing; each SmartJsonLD
            instance is expected to have a default context associated.
        :param: new_context the context to use for formatted publishing,
            usually supplied by the client; used by the 'compacted', 'framed',
            and 'normalized' formats.
        :param: format the publishing format; can be 'full', 'inline',
            'compacted', 'expanded', 'flattened', 'framed' or 'normalized'.
            Note that 'full' and 'inline' are synonims, referring to the
            document form which includes the context; for more information see:
            [http://www.w3.org/TR/json-ld/]
        """
        from pyld import jsonld

        if isinstance(context, six.string_types):
            ctx = self.get_context(context)
        elif isinstance(context, dict):
            ctx = context
        else:
            raise TypeError('JSON-LD context must be a string or dictionary')

        try:
            doc = self.translate(context, ctx)
        except NotImplementedError:
            # model does not require translation
            doc = self.dumps(clean=True)

        doc["@context"] = ctx

        if format in ["full", "inline"]:
            return doc
        if format == "compacted":
            return jsonld.compact(doc, new_context)
        elif format == "expanded":
            return jsonld.expand(doc)
        elif format == "flattened":
            return jsonld.flatten(doc)
        elif format == "framed":
            return jsonld.frame(doc, new_context)
        elif format == "normalized":
            return jsonld.normalize(doc, new_context)
        raise ValueError('Invalid JSON-LD serialization format')
