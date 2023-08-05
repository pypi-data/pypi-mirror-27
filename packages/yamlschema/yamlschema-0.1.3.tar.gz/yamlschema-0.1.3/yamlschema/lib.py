"""
Validate a YAML file
"""

import os
import sys

import yaml

from jsonschema import validate, ValidationError, FormatChecker

from codado.tx import Main


class ValidateYAML(Main):
    """
    Validate a yaml file based on a schema
    """
    synopsis = "path/to/file.yml path/to/schema.yml"
    optFlags = [
        ['schema', None, 'Display normalized schema from file']
    ]
    optParameters = []

    def parseArgs(self, yamlFile, yamlSchema):
        if not os.access(yamlFile, os.R_OK):
            raise OSError("Cannot read config file %s" % yamlFile)
        if not os.access(yamlSchema, os.R_OK):
            raise OSError("Cannot read schema file %s" % yamlSchema)

        self['yamlFile'] = yamlFile
        self['yamlSchema'] = yamlSchema

    def postOptions(self):
        """
        Validate config file
        """
        print >>sys.stderr, "Validating {}\n".format(self['yamlFile'])
        res = validateYAML(self['yamlFile'], self['yamlSchema'])
        print >>sys.stderr, "{} is valid\n".format(self['yamlFile'])
        return res


def validateYAML(yamlFile, yamlSchema):
    """
    Validate yaml file based off of a schema
    """
    contents = yaml.load(open(yamlFile))
    schema = yaml.load(open(yamlSchema))
    try:
        validate(contents, schema, format_checker=FormatChecker())
        return True
    except ValidationError, ve:
        raise ve