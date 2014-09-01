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

    def get_source(self, path):
        """Get the file content and reload helper as a ``(source, uptodate)``
        tuple.

        The first part of the returned tuple is file content as unicode
        string. If file does not exist then empty string returned.

        The last part is `uptodate` function. When autoreload is enabled
        it's always called to check if the file content changed. If it returns
        `False` the file will be reloaded.

        :param path: The path to file.
        """
        if not os.path.exists(path):
            return ''

        with open(path, 'rb') as fileobj:
            source = fileobj.read().decode('utf-8')

        mtime = os.path.getmtime(path)

        def uptodate():
            try:
                return os.path.getmtime(path) == mtime
            except IOError:
                return False

        return source, uptodate
