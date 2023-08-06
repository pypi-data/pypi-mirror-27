import econfig
import os
import pytest


@pytest.fixture()
def env():
    econfig.reset()


def test_parse(env):
    econfig.register(
        name='MY_CONFIGURATION',
        type=econfig.types.int,
        destination='foo.bar')
    os.environ['MY_CONFIGURATION'] = '200'
    errors, settings = econfig.parse()
    assert len(errors) == 0
    assert settings['foo']['bar'] == 200


def test_parse_error(env):
    econfig.register(
        name='MY_CONFIGURATION',
        type=econfig.types.int,
        destination='foo.bar')
    os.environ['MY_CONFIGURATION'] = 'hello'
    errors, settings = econfig.parse()
    assert len(errors) == 1
    assert 'foo' not in settings


def test_parse_json(env):
    econfig.register(
        name='MY_CONFIGURATION',
        type=econfig.types.json,
        destination='foo.bar')
    os.environ['MY_CONFIGURATION'] = '{"foo": "bar"}'
    errors, settings = econfig.parse()
    assert len(errors) == 0
    assert settings['foo']['bar']['foo'] == 'bar'


def test_list_append_addressing(env):
    econfig.register(
        name='MY_CONFIGURATION',
        destination='foo.bar[]')
    os.environ['MY_CONFIGURATION'] = 'foobar'
    errors, settings = econfig.parse()
    assert len(errors) == 0
    assert len(settings['foo']['bar']) == 1
    assert settings['foo']['bar'][0] == 'foobar'


def test_list_value_assignment_list(env):
    econfig.register(
        name='MY_CONFIGURATION',
        destination='foo.bar[0].foo.bar')
    os.environ['MY_CONFIGURATION'] = 'foobar'
    errors, settings = econfig.parse()
    assert len(errors) == 0
    assert len(settings['foo']['bar']) == 1
    assert settings['foo']['bar'][0]['foo']['bar'] == 'foobar'


def test_when_exists(env):
    econfig.register(
        name='MY_CONFIGURATION',
        destination='foo',
        type=econfig.types.when_exists({'foo': 'bar'}))
    econfig.register(
        name='MY_CONFIGURATION_MISSING',
        destination='bar',
        type=econfig.types.when_exists({'foo': 'bar'}))
    os.environ['MY_CONFIGURATION'] = 'foobar'
    errors, settings = econfig.parse()
    assert len(errors) == 0
    assert settings['foo'] == {'foo': 'bar'}
    assert 'bar' not in settings


def test_format_options(env):
    econfig.register(
        name='MY_CONFIGURATION_1',
        destination='foo')
    econfig.register(
        name='MY_CONFIGURATION_2',
        destination='bar',
        type=econfig.types.when_exists({'foo': 'bar'}))

    formatting = econfig.format_options()
    assert "<when_exists: {'foo': 'bar'}>" in formatting
