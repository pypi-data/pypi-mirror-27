from collections import OrderedDict
from contextlib import contextmanager
from copy import deepcopy
import re
import sys


class Attribute(object):
    def __init__(self, name, group, namespace=None, value=None,
                 commented=False, deprecated=False):
        self.name = name
        self.group = group
        self.namespace = namespace
        self.value = value
        self.commented = commented
        self.deprecated = deprecated
        self.new = None

    def deprecated_by(self, attr):
        self.deprecated = True
        self.new = attr

    def __key(self):
        return self.name, self.group

    def __eq__(self, other):
        if isinstance(other, Attribute):
            return self.__key() == other.__key()
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__key())


class Config(object):
    """
    Configure object which mapped to one config file. 
    
    It parses the config file at first and has attributes which extracted 
    with the pre-defined patterns.
    """
    # Any valid name
    NAME_REGEX = r'[a-zA-Z0-9._-]+'
    # All characters only except newline. $ is for empty.
    ALL_REGEX = r'$|[^\n]+'

    # Patterns below are appeared mutually exclusive
    PATTERNS = {
        # Namespace pattern is Like '# From nova.api', '# From nova.conf'
        'namespace':
            f'# From (?P<namespace>{NAME_REGEX})',
        # Group pattern is like '[DEFAULT]', '[api]', '[glance]'
        'group':
            f'\[(?P<group>{NAME_REGEX})\]',
        # Deprecated attributes
        'deprecated':
            f'# Deprecated group/name - \[(?P<group>{NAME_REGEX})\]/(?P<name>{NAME_REGEX})',
        # Modified attribute pattern is without being commented
        'modified':
            f'^(?P<name>{NAME_REGEX}) = (?P<value>{ALL_REGEX})',
        # Commented attribute pattern start with '#'
        'commented':
            f'^#(?P<name>{NAME_REGEX}) =[ ]*(?P<value>{ALL_REGEX})',
    }

    def __init__(self, name):
        self.name = name
        self.attrs = {}
        self.deprecated = {}

        def create(**kwargs):
            properties = kwargs['properties']
            context = kwargs['context']

            key = (properties['name'], context['group'])
            if key in self.attrs:
                entry = self.attrs[key]
                value = properties['value']

                if type(entry.value) is list:
                    entry.value.append(value)
                else:
                    past = entry.value
                    entry.value = [past, value]
                return

            entry = Attribute(**properties, **context)
            self.attrs[key] = entry

            while context['deprecated']:
                self.deprecated[context['deprecated'].pop(0)] = entry

        self._iterate(Config.PATTERNS, {'commented': create, 'modified': create})

    def attributes(self, name=None, group=None, namespace=None, commented=None):
        """ 
        Get all attributes(commented/modified) or one attribute by name.
        
        Args:
            name (str): attribute name.
            group (str): group name.
            namespace (str): namespace name.
            commented (bool): whether attributes are commented or not.

        Returns:
            list: List of Attributes.
        """

        result = self.attrs.values()
        values = {'name': name, 'group': group,
                  'namespace': namespace, 'commented': commented}
        for key, value in values.items():
            if value is None:
                continue
            result = [a for a in result if getattr(a, key) == value]

        return result[0] if len(result) == 1 else result

    def substitute(self, attr):
        """
        Get new attribute which replace deprecated attribute.

        Args:
            attr (Attribute): deprecated attribute.

        Returns:
            Attribute: new attribute which substitute deprecated one.
        """

        return self.deprecated.get(attr, None)

    def update(self, attribute, value, commented=None):
        """
        Iteratively call specified function with the properties which are 
        extracted by matched pattern.
        
        Args:
            attribute (Attribute): patterns to be extracted.
            value (str): functions to be called.
            commented (bool): whether the attribute are commented or not.
        
        Returns:
            Attribute or None: updated Attribute if found or None.
            
        """

        key = (attribute.name, attribute.group)
        if key in self.attrs:
            attr = self.attrs[key]
            attr.value = value
            if commented is not None:
                attr.commented = commented
            return self.attrs[key]

        return None

    def _iterate(self, pattern, func):
        """
        Iteratively call specified function with the properties which are 
        extracted by matched pattern.
        
        Args:
            pattern (Dict of Patterns): patterns to be extracted.
            func (Dict of functions): callback functions to be called.
        """

        @contextmanager
        def property_context(context, name, values):

            if name in ('group', 'namespace'):
                context[name] = values[pattern]
            elif name in 'commented':
                context[name] = True
            elif name in 'deprecated':
                context['deprecated'].append(Attribute(**values, deprecated=True))

            yield context

            context['commented'] = False

        current = {
            'group': None,
            'namespace': None,
            'deprecated': [],
            'commented': False
        }

        for pattern, match in self._extract(pattern):
            properties = match.groupdict()
            with property_context(current, pattern, properties) as current:
                if pattern in func:
                    func[pattern](match=match, properties=properties,
                                  context=current)

    def write(self, file=sys.stdout):
        """
        Write current config contents into file.
        
        Args:
            file (File): Defaults to stdout.
        """

        attrs = deepcopy(self.attrs)

        def write_through(**kwargs):
            match = kwargs['match']
            print(match.group(0), file=file)

        def replace(**kwargs):
            match = kwargs['match']
            context = kwargs['context']

            attr = attrs[(match['name'], context['group'])]
            if attr.commented:
                print(match.group(0), file=file)
                return

            name = match.group(1)
            value = attr.value
            if type(attr.value) is list:
                value = attr.value.pop(0)

            line = re.sub(Config.PATTERNS['commented'],
                          f"{name} = {value}", match.group(0))
            print(line, file=file)

        pattern = OrderedDict(Config.PATTERNS.items())
        pattern['all'] = Config.ALL_REGEX

        self._iterate(pattern, {'all': write_through,
                                'deprecated': write_through,
                                'group': write_through,
                                'namespace': write_through,
                                'commented': replace,
                                'modified': replace})

    def _extract(self, patterns):
        """
        Extract attributes which defined by specific patterns in file.
        
        Args:
            patterns (Dict of Patterns): Patterns to be matched.

        Returns:
            Generator: Generate matched pattern name and match object.
        """

        with open(self.name, 'r') as file:
            for line in file:
                for name, pattern in patterns.items():
                    match = re.match(pattern, line)
                    if match:
                        yield name, match
                        break
