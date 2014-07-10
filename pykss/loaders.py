#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
