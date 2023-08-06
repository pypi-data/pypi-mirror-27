import os

import nbformat


def read(root, filename):
    root = os.path.dirname(os.path.abspath(root))

    basename = None
    while basename != 'tests':
        root, basename = os.path.split(root)
        if basename == '':
            raise ValueError('Could not find `tests` directory.', root)

    path = os.path.join(root, basename, 'resources', filename)
    path = os.path.abspath(path)

    with open(path) as f:
        if path.endswith('.ipynb'):
            return nbformat.read(f, as_version=4)
        else:
            return f.read()
