Env Config
==========

Python package to manage configuration from environment variables.

This package is designed to be used to help in configuration management with
python docker containers.


Defining configuration
----------------------

econfig provides simple data types to define configuration with::

    import econfig
    econfig.register(
      name='MY_CONFIGURATION_NUMBER',
      type=econfig.types.int,
      destination='foo.bar')
    econfig.register(
        name='MY_CONFIGURATION_NUMBER',
        type=econfig.types.json,
        destination='foo.json')
    errors, settings = econfig.parse()
    settings == {
      "foo": {
        "bar": 5
      },
      "json": {
        "some": "value"
      }
    }


Types
-----

- int
- float
- bool
- exists
- json
- when_exists: callable type that will provide value when env variable exists


Destination types
-----------------

- `foo.bar`: automatic key value dictionary creation
- `foo[]`: append value to list
- `foo[0]`: address item in list
- `foo[0].bar`: address dictionary item in list
