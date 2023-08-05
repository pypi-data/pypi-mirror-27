#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_hello_world
----------------------------------

Tests for `hello_world` module.
"""

import unittest

import hello_world.cli


class TestHello_world(unittest.TestCase):

    def setUp(self):
        self.hello_message = "Hello, World!"

    def test_prints_hello_world(self):
        output = hello_world.cli.hello()
        print(output, self.hello_message)
        assert output == self.hello_message
