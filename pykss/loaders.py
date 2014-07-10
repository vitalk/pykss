#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class Loader(object):
    """Base class for all loaders. Uses to load content from files or other
    sources.
    """

    def load(self, name):
        """Loads data."""
        raise NotImplementedError

    def get_source(self, name):
        raise NotImplementedError

    def list_files(self):
        """Iterates over all files. Must be implemented in subclasses."""
        raise NotImplementedError('this loader does not implement '
                                  'iterating over all files')


class FileSystemLoader(Loader):
    """Loads files from the file system.

    The loader may take path to files as string or list::

        >>> loader = FileSystemLoader('/dir/to/lookup')
        >>> loader = FileSystemLoader(['/dir/to/lookup', '/other/dir'])

    :param searchpath: The root directory or directories to lookup files.
    """

    def __init__(self, searchpath):
        if not isinstance(searchpath, (list, tuple)):
            searchpath = searchpath,
        self.searchpath = tuple(searchpath)

    def list_files(self):
        """Iterates over all files in searchpaths directories."""
        found = set()
        for searchpath in self.searchpath:
            walk_dir = os.walk(searchpath)
            for dirpath, dirnames, filenames in walk_dir:
                for filename in filenames:
                    path = os.path.join(dirpath, filename)
                    if path not in found:
                        found.add(path)
        return sorted(found)
