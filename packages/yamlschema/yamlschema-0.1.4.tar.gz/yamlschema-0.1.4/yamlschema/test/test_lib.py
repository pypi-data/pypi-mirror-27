"""
Tests for YAML file validation
"""

import sys
import os

from jsonschema import ValidationError

from codado import fromdir

from pytest import fixture, raises

from mock import patch

from yamlschema.lib import ValidateYAML


@fixture
def options():
    options = ValidateYAML()
    options['yamlSchema'] = fromdir(__file__)('test_config.schema.yml')
    return options


@fixture
def configGood():
    return fromdir(__file__)('test_config.yml')
    

@fixture
def configBad():
    return fromdir(__file__)('test_config_bad.yml')


def test_postOptionsOk(options, configGood):
    """
    Does a good config pass?
    """
    options['yamlFile'] = configGood
    pOut = patch.object(sys, 'stdout', autospec=True)
    pErr = patch.object(sys, 'stderr', autospec=True)
    with pOut, pErr:
        x = options.postOptions()
        assert x == True


def test_postOptionsBad(options, configBad):
    """
    Does a bad config fail?
    """
    pOut = patch.object(sys, 'stdout', autospec=True)
    pErr = patch.object(sys, 'stderr', autospec=True)
    options['yamlFile'] = configBad

    with pOut, pErr:
        raises(ValidationError, options.postOptions)


def test_parseArgs(options):
    """
    Do we check permissions on files and report those errors?
    """
    with patch.object(os, 'access', return_value=False):
        raises(OSError, options.parseArgs, 'adafds', 'fdsa')

    with patch.object(os, 'access', side_effect=[True, False]):
        raises(OSError, options.parseArgs, 'adafds', 'fdsa')

    with patch.object(os, 'access', return_value=True):
        options.parseArgs('cheeses', 'meats')
        assert options['yamlFile'] == 'cheeses'
        assert options['yamlSchema'] == 'meats'

