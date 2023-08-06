import click
import collections
import sys
import textwrap
from . import config


@click.group()
def main():
    """Check and upgrade OpenStack configure files"""
    print("OpenStack config upgrade")


@main.command()
@click.argument('FILE1', type=click.Path(exists=True))
@click.argument('FILE2',type=click.Path(exists=True))
@click.option('-v', '--verbose', count=True, help='Show details')
def check(file1, file2, verbose):
    """
    Check difference between two config files. FILE1, FILE2.
    
    Args:
        file1 (str): name of file which comparison based on.
        file2 (str): name of file which is compared to.
        verbose (int): verbosity.
    """

    category = _categorize(config.Config(file1), config.Config(file2))
    for name, attrs in category._asdict().items():
        _print(attrs, name, verbose)


@main.command()
@click.argument('FILE1', type=click.Path(exists=True))
@click.argument('FILE2', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.File('w'),
              help='Output file. (Defaults to stdout)', default=sys.stdout)
def upgrade(file1, file2, output):
    """
    Upgrade config by comparing two config files. FILE1, FILE2.
    
    Args:
        file1 (str): name of file which comparison based on.
        file2 (str): name of file which is compared to.
        output (str): name of output file.
    """

    config1 = config.Config(file1)
    config2 = config.Config(file2)

    category = _categorize(config1, config2)
    for attr in category.unchanged:
        config2.update(attr, value=attr.value, commented=False)

    for attr in category.changed:
        config2.update(attr.new, value=attr.value, commented=False)

    config2.write(output)


def _categorize(config1, config2):
    """
    Upgrade config by comparing two config files. FILE1, FILE2.
    
    Args:
        config1 (Config): Config object which comparison based on.
        config2 (Config): Config object which is compared to.
        
    Returns:
        namedtuple: Named Tuple of set of attributes. Attributes belong to 
                    'added', 'removed', 'unchanged', 'changed', 'ambiguous'
    """

    groups = _compare(config1, config2)
    categories = []

    for group in groups:
        result = sorted(group, key=lambda x: (x.group, x.namespace, x.name))
        categories.append([x for x in result if x.commented is False])

    Category = collections.namedtuple(
        'Category',
        ['added', 'removed', 'unchanged', 'changed', 'ambiguous']
    )

    return Category._make(categories)


def _compare(config1, config2):
    """
    Compare between two config FILES.
    
    Args:
        config1 (Config): Config object which comparison based on.
        config2 (Config): Config object which is compared to.
        
    Returns:
        tuple: Tuple of set of attributes which belongs to specific state.
    """

    attr1 = set(config1.attributes())
    attr2 = set(config2.attributes())

    added = attr2 - attr1
    removed = attr1 - attr2
    unchanged = attr1 - removed

    changed = set()
    ambiguous = set()
    for attr in removed:
        new = config2.substitute(attr)
        if new is not None:
            attr.deprecated_by(new)
            changed.add(attr)
            continue

        candidates = [x for x in added if x.name == attr.name]
        if len(candidates) == 1:
            candidate = candidates[0]
            if attr.group == 'DEFAULT' or attr.group == candidate.group:
                attr.deprecated_by(candidate)
                changed.add(attr)
            else:
                ambiguous.add(attr)
        elif len(candidates) > 1:
            ambiguous.add(attr)

    added = added - changed - ambiguous
    removed = removed - changed - ambiguous

    return added, removed, unchanged, changed, ambiguous


def _print(attrs, state=None, verbose=0):
    """
    Print attributes which has specific states.
    
    Args:
        attrs (set): Set of attributes.
        state (str): State name which attributes belong to.
        verbose (int): verbosity.
    """

    def formatted(chars, color='', indent=0):
        codes = {
            'purple': '\033[95m',
            'blue': '\033[94m', 'green': '\033[92m',
            'end': '\033[0m'
        }

        start = codes.get(color, '')
        end = codes['end'] if color else ''

        return textwrap.indent(start + chars + end, ' ' * 4 * indent)

    if state is not None:
        print(formatted(f'\n{state.title()} attributes:', 'green'))

    current = {'namespace': '', 'group': ''}
    for attr in attrs:
        if current['group'] != attr.group:
            print(formatted(attr.group, 'blue', 1))
            current['group'] = attr.group

        addition = ''
        if attr.deprecated:
            addition = f' -> [{attr.new.group}]/{attr.new.name}'

        if verbose > 0:
            if current['namespace'] != attr.namespace:
                print(formatted(attr.namespace, 'purple', 2))
                current['namespace'] = attr.namespace
            if attr.deprecated:
                addition = addition + f' ({attr.new.namespace})'

        if verbose > 1:
            addition = addition + f' = {attr.value}'

        print(formatted(attr.name + addition, indent=3 if verbose > 0 else 2))

if __name__ == '__main__':
    main()
