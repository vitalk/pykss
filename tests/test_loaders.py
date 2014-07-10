#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import shutil
import tempfile

from pykss.loaders import Loader
from pykss.loaders import FileSystemLoader


class TempdirHelper(object):
    """Provide temporary directory for each test suite."""

    default_files = ()

    def setUp(self):
        self._tempdir = tempfile.mkdtemp()
        self._create_files(self.default_files)

    def tearDown(self):
        shutil.rmtree(self._tempdir)

    @property
    def tempdir(self):
        """Use read-only property to prevent tempdir removal."""
        return self._tempdir

    def _create_files(self, files):
        """Create files in temporary directory. Use list to create empty
        files or use dictionary values to write content to them.
        """
        if not hasattr(files, 'items'):
            files = {filename: '' for filename in files}

        for filename, content in files.items():
            self._create_file(self.path(filename), content)

    def _create_file(self, path, content):
        """Create a file. Ensure directory is exists."""
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.mkdir(directory)
        with open(path, 'w') as outfile:
            outfile.write(content)

    def path(self, filename):
        """Returns absolute path for given filename in tempdir."""
        return os.path.join(self.tempdir, filename)


class LoaderTestCase(unittest.TestCase):

    def setUp(self):
        self.loader = Loader()

    def test_load(self):
        self.assertRaises(NotImplementedError, self.loader.load, 'name')

    def test_list_files(self):
        self.assertRaises(NotImplementedError, self.loader.list_files)

    def test_get_source(self):
        self.assertRaises(NotImplementedError, self.loader.get_source, 'name')


class FileSystemLoaderTestCase(unittest.TestCase, TempdirHelper):

    default_files = (
        'foobar',
        'foo/bar',
        'foo/baz',
        'bar/baz',
    )

    def setUp(self):
        TempdirHelper.setUp(self)
        self.loader = FileSystemLoader(self.tempdir)

    def test_searchpath_as_string(self):
        self.assertEqual(self.loader.searchpath, (self.tempdir,))

    def test_searchpath_as_list(self):
        loader = FileSystemLoader([self.tempdir])
        self.assertEqual(loader.searchpath, (self.tempdir,))

    def test_list_files(self):
        expected = sorted(map(self.path, self.default_files))
        self.assertEqual(self.loader.list_files(), expected)
