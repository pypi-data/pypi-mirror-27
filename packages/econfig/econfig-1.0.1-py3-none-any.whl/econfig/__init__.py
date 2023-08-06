import json
import logging
import os


logger = logging.getLogger('envconfig')


_registrations = []


def reset():
    del _registrations[:]


class ConfigurationError(Exception):
    pass


class ParseError(Exception):
    pass


class ValueParser:

    def __init__(self, name=None):
        if name:
            self.name = name

    def __call__(self, val):
        return val

    def __str__(self):
        return f'<{self.name}>'


class DyanamicValueParser(ValueParser):

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, val):
        try:
            return self.func(val)
        except Exception:
            logger.warn(f'Error parsing {self.name} value', exc_info=True)
            raise ParseError(f'Could not parse {self.name} {val}')


class WhenExists(ValueParser):
    name = 'when_exists'

    def __call__(self, val):
        return MetaWhenExists(self, val)


class MetaWhenExists(WhenExists):
    def __init__(self, parent, val):
        self.parent = parent
        self.val = val

    def __call__(self, val):
        return self.val

    def __str__(self):
        return f'<{self.name}: {self.val}>'


class types:
    int = DyanamicValueParser('int', int)
    float = DyanamicValueParser('float', float)
    json = DyanamicValueParser('json', json.loads)
    string = ValueParser('string')
    bool = DyanamicValueParser('bool', lambda val: val.lower() in ('1', 'true', True, 1))
    exists = DyanamicValueParser('bool', lambda val: True)
    when_exists = WhenExists()


def register(name=None, destination=None, type=types.string, required=False,
             description='', default=None):
    if name is None:
        raise ConfigurationError('name missing')
    if type is None:
        raise ConfigurationError('type missing')
    if destination is None:
        raise ConfigurationError('destination missing')
    if default is not None and not isinstance(default, str):
        raise ConfigurationError(f'Default value must be a string, got: {default}')
    _registrations.append({
        'name': name,
        'type': type,
        'destination': destination,
        'required': required,
        'description': description,
        'default': default
    })


def get_context(path, context):
    for name in path.split('.'):
        if name.endswith(']'):
            # list type here...
            real_name = name.split('[')[0]
            if real_name not in context:
                context[real_name] = []

            context = context[real_name]

            if not name.endswith('[]'):
                # addressing specific object in list
                index = int(name.split('[')[1].strip(']'))
                while True:
                    try:
                        context = context[index]
                        break
                    except IndexError:
                        context.append({})
        else:
            if name not in context:
                context[name] = {}
            context = context[name]
    return context


def parse(data=None):
    errors = {}
    if data is None:
        data = {}
    for config in _registrations:
        env_name = config['name']
        val = os.environ.get(env_name, config['default'])
        if val is None:
            if config['required']:
                errors[env_name] = ParseError('Value is required')
            continue
        try:
            parsed_value = config['type'](val)
        except ParseError as ex:
            errors[env_name] = ex
            continue

        base_name = '.'.join(config['destination'].split('.')[:-1])
        if base_name:
            context = get_context(base_name, data)
        else:
            context = data
        dest_name = config['destination'].split('.')[-1]
        if '[' in dest_name:
            # list type here...
            context = get_context(dest_name, context)
            context.append(parsed_value)
        else:
            context[dest_name] = parsed_value
    return errors, data


_indent = 4

def format_options():
    options = []
    for config in _registrations:
        formatted = config['name'] + ':'
        if config['description']:
            formatted += f''': {config['description']}'''
        formatted += f'''
{_indent * ' '}Destination: {config['destination']}
{_indent * ' '}Type: {config['type']}'''
        if config['default'] is not None:
            formatted += (_indent * ' ') + f'''
{_indent * ' '}Default: {config['default']}'''

        options.append(formatted)

    return '''
Environment Variable Options
----------------------------

{}'''.format('\n'.join(options))
