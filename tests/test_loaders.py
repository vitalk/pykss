#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from pykss.loaders import Loader


class LoaderTestCase(unittest.TestCase):

    def setUp(self):
        self.loader = Loader()

    def test_load(self):
        self.assertRaises(NotImplementedError, self.loader.load, 'name')

    def test_list_files(self):
        self.assertRaises(NotImplementedError, self.loader.list_files)

    def test_get_source(self):
        self.assertRaises(NotImplementedError, self.loader.get_source, 'name')
