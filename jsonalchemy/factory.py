import json

from jsonschema import Draft4Validator


def model_factory(base_class, schema_url):
    class Model(object):
        __schema__ = {}
        my_field = "foo"

    with open(schema_url, "r") as schema_file:
        schema = json.loads(schema_file.read())
        validator = Draft4Validator(schema)

        Model.__schema__ = schema

    return Model
