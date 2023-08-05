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


def names(import_expr):
    """Get referenced names from an import expression.
    """
    if isinstance(import_expr, ast.Import):
        return [alias.name for alias in import_expr.names]
    else:  # ImportFrom
        return [f'{import_expr.module}.{alias.name}' for alias in import_expr.names]


def recursively_collect_imports(expr, acc=None):
    if acc is None:
        acc = []
    for subexpr in expr.body:
        if isinstance(subexpr, (ast.Import, ast.ImportFrom)):
            acc.append(subexpr)
        elif hasattr(subexpr, 'body'):
            recursively_collect_imports(subexpr, acc)
    return acc


def imported_names(source_path):
    """Find top-level dependencies for module, recursing into expression bodies.

    Doesn't try to do anything smart with conditional imports; it includes all
    conditional branches.
    """
    with open(source_path) as f:
        source = f.read()
    expr = ast.parse(source)
    imports = recursively_collect_imports(expr)
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
    parts[-1] = os.path.splitext(parts[-1])[0]
    return '.'.join(parts)


def build_graph(package_name):
    graph = {}

    def normalize_name(imported_name):
        """Given some imported name ``foo.bar.baz``, where ``foo`` is the
        package under inspection, find the longest subname that maps to a module
        or package. In other words, discard names imported from _within_ a
        module, like ``foo.bar.baz.SomeClass``.
        """
        parts = imported_name.split('.')
        if package_name != parts[0]:
            return imported_name
        while parts:
            module_path = os.path.join(*parts) + '.py'
            package_path = os.path.join(*(parts + ['__init__.py']))
            if os.path.exists(module_path) or os.path.exists(package_path):
                ret = '.'.join(parts)
                return ret
            parts.pop()
        # No part of the name corresponded to a file. We're not a compiler, so
        # just pretend we didn't see it.
        return imported_name


    for root, dirs, files in os.walk(package_name):
        for file in files:
            if not file.endswith('.py'):
                continue
            module_path = os.path.join(root, file)
            names = set(normalize_name(name) for name in imported_names(module_path))
            graph[module_name(module_path, package_name)] = names

    return graph


def filter_dependencies(graph, package_name, included_types):
    def root_name(module_name):
        return module_name.split('.', 1)[0]

    def is_builtin(imported_name):
        return root_name(imported_name) in BUILTINS

    def is_3rd_party(imported_name):
        return root_name(imported_name) not in BUILTINS \
            and root_name(imported_name) != package_name

    def is_internal(imported_name):
        return root_name(imported_name) == package_name

    def exclude(dep):
        return (('builtin' not in included_types and is_builtin(dep)) or
                ('3rd-party' not in included_types and is_3rd_party(dep)) or
                ('internal' not in included_types and is_internal(dep)))

    return {mod: [dep for dep in deps if not exclude(dep)]
            for mod, deps in graph.items()}


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

    if not os.path.exists(os.path.join(args.package_root, '__init__.py')):
        raise Exception(f'not a package: {args.package_root}')

    # this is kind of gross, but it simplifies path resolution (we can use
    # package directory and name interchangeably)
    os.chdir(os.path.dirname(args.package_root))
    package_name = os.path.basename(args.package_root)

    includes = set([args.includes]) if args.includes else set(DEP_TYPES) - set(args.excludes)

    graph = build_graph(package_name)
    graph = filter_dependencies(graph, package_name, includes)
    graph = normalize_module_names(graph, args.package_module_name_segments, args.dependency_module_name_segments)
    print_graph(graph, format=args.format)


if __name__ == '__main__':
    main()
