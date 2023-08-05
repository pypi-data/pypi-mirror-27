#!/usr/bin/env python3
"""
Explore dependencies of a package by parsing its imports.
"""

from collections import defaultdict
from functools import reduce
import ast
import os
import os.path
import sys


# from https://docs.python.org/3/py-modindex.html
BUILTINS = set('''
__future__ __main__ _dummy_thread _thread abc aifc argparse array ast asynchat
asyncio asyncore atexit audioop base64 bdb binascii binhex bisect builtins bz2
calendar cgi cgitb chunk cmath cmd code codecs codeop collections colorsys
compileall concurrent configparser contextlib copy copyreg cProfile crypt csv
ctypes curses datetime dbm decimal difflib dis distutils doctest dummy_threading
email encodings ensurepip enum errno faulthandler fcntl filecmp fileinput
fnmatch formatter fpectl fractions ftplib functools gc getopt getpass gettext
glob grp gzip hashlib heapq hmac html http imaplib imghdr imp importlib inspect
io ipaddress itertools json keyword lib2to3 linecache locale logging lzma
macpath mailbox mailcap marshal math mimetypes mmap modulefinder msilib msvcrt
multiprocessing netrc nis nntplib numbers operator optparse os ossaudiodev
parser pathlib pdb pickle pickletools pipes pkgutil platform plistlib poplib
posix pprint profile pstats pty pwd py_compile pyclbr pydoc queue quopri random
re readline reprlib resource rlcompleter runpy sched secrets select selectors
shelve shlex shutil signal site smtpd smtplib sndhdr socket socketserver spwd
sqlite3 ssl stat statistics string stringprep struct subprocess sunau symbol
symtable sys sysconfig syslog tabnanny tarfile telnetlib tempfile termios test
textwrap threading time timeit tkinter token tokenize trace traceback
tracemalloc tty turtle turtledemo types typing unicodedata unittest urllib uu
uuid venv warnings wave weakref webbrowser winreg winsound wsgiref xdrlib xml
xmlrpc zipapp zipfile zipimport zlib
'''.split())


def is_package(pkg_path):
    return os.path.exists(os.path.join(pkg_path, '__init__.py'))


def names(import_):
    """Get referenced module names from an import statement.
    """
    if isinstance(import_, ast.Import):
        return [alias.name for alias in import_.names]
    return [f'{import_.module}.{alias.name}' for alias in import_.names]


def module_imports(module_path):
    """Find top-level dependencies for module, recursing into expression bodies.

    Doesn't try to do anything smart with conditional imports; it includes all
    conditional branches.
    """
    with open(module_path) as f:
        source = f.read()
    module = ast.parse(source, module_path)

    def recursively_collect_imports(expr, acc=[]):
        for subexpr in expr.body:
            if isinstance(subexpr, (ast.Import, ast.ImportFrom)):
                acc.append(subexpr)
            elif hasattr(subexpr, 'body'):
                recursively_collect_imports(subexpr, acc)
        return acc

    imports = recursively_collect_imports(module)
    return reduce(list.__add__, [names(imp) for imp in imports], [])


# https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch04s16.html
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def module_name(module_path, root_path):
    """Get module name from its path and the path of its containing package.

    > module_name("env/lib/site-packages/foo/bar/baz.py", "env/lib/site-packages/foo")
    foo.bar.baz
    """
    module_relpath = os.path.relpath(module_path, os.path.dirname(root_path))
    parts = splitall(module_relpath)
    if parts[-1] == '__init__.py':
        del parts[-1]
    else:
        parts[-1] = os.path.splitext(parts[-1])[0]
    return '.'.join(parts)


def normalize_module_names(graph, num_pkg_segments=None, num_dep_segments=None):
    """Normalize module names in dependency graph.

    Args:
        num_pkg_segments (int): if specified, truncate module names of the
            inspected package to the given number of namespace segments.
        num_dep_segments (int): if specified, truncate module names of the
            inspected package's dependencies to the given number of namespace
            segments.
    """
    def normalize_name(module_name, depth):
        return '.'.join(module_name.split('.')[:depth])
    normalized = defaultdict(set)
    for mod_name, deps in graph.items():
        normalized[normalize_name(mod_name, num_pkg_segments)].update(normalize_name(dep, num_dep_segments) for dep in deps)
    return normalized


def build_graph(root_path, depth=None):
    graph = {}

    for root, dirs, files in os.walk(root_path):
        for file in files:
            if not file.endswith('.py'):
                continue
            module_path = os.path.join(root, file)
            graph[module_name(module_path, root_path)] = module_imports(module_path)
        # if '__pycache__' in dirs:
        #     dirs.remove('__pycache__')

    if depth is not None:
        return normalize_graph(graph, depth)

    return graph


def filter_dependencies(graph, package_name, includes):
    def root_name(module_name):
        return module_name.split('.', 1)[0]

    def is_builtin(module_name):
        return root_name(module_name) in BUILTINS

    def is_3rd_party(module_name):
        return root_name(module_name) not in BUILTINS \
            and root_name(module_name) != package_name

    def is_internal(module_name):
        return root_name(module_name) == package_name

    def exclude(dep):
        return (('builtin' not in includes and is_builtin(dep)) or
                ('3rd-party' not in includes and is_3rd_party(dep)) or
                ('internal' not in includes and is_internal(dep)))

    return {mod: [dep for dep in deps if not exclude(dep)]
            for mod, deps in graph.items()}


def print_graph(graph, format):
    if format == 'tree':
        for mod, deps in sorted(graph.items()):
            sep = '\n  - '
            names = sep.join(sorted(deps))
            print(f'{mod}{sep if names else ""}{names}')
    elif format == 'tsort':
        for mod, deps in graph.items():
            for dep in deps:
                print(f'{mod} {dep}')
    else:
        NotImplemented

DEP_TYPES = ('builtin', '3rd-party', 'internal')
OUTPUT_FORMATS = ('tree', 'tsort')

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Explore dependencies of a package by parsing its imports.')
    parser.add_argument('-n', '--package-module-name-segments', type=int, metavar='<num>',
                        help='truncate module names of inspected package to given number of segments (and consolidate imports)')
    parser.add_argument('-m', '--dependency-module-name-segments', type=int, metavar='<num>',
                        help='truncate module names of dependencies to given number of segments (and deduplicate)')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--exclude', dest='excludes', choices=DEP_TYPES, action='append', metavar='<type>', default=(),
                       help=f'exclude various kinds of dependencies from output ({", ".join(DEP_TYPES)})')
    group.add_argument('-o', '--only', dest='includes', choices=DEP_TYPES, metavar='<type>',
                       help=f'include only dependencies of the given type ({", ".join(DEP_TYPES)})')

    parser.add_argument('-f', '--format', dest='format', choices=OUTPUT_FORMATS, metavar='<format>', default='tree',
                        help=f'graph output format ({", ".join(OUTPUT_FORMATS)})')

    parser.add_argument('package_root', metavar='</path/to/package>', help='path to package root')

    args = parser.parse_args()

    if not is_package(args.package_root):
        raise Exception(f'not an inspectable package: {args.package_root}')

    includes = set([args.includes]) if args.includes else set(DEP_TYPES) - set(args.excludes)

    graph = build_graph(args.package_root)
    graph = normalize_module_names(graph, args.package_module_name_segments, args.dependency_module_name_segments)
    graph = filter_dependencies(graph, os.path.basename(args.package_root), includes)
    print_graph(graph, format=args.format)


if __name__ == '__main__':
    main()
