from unittest import TestCase
from mlx.json_to_mako import json_to_mako_wrapper


class TestJsonToMako(TestCase):

    def test_help(self):
        with self.assertRaises(SystemExit) as ex:
            json_to_mako_wrapper(['--help'])
        self.assertEqual(0, ex.exception.code)

    def test_version(self):
        with self.assertRaises(SystemExit) as ex:
            json_to_mako_wrapper(['--version'])
        self.assertEqual(0, ex.exception.code)

    def test_example_ok(self):
        json_to_mako_wrapper(['--input', 'example/family.json',
                              '--input', 'example/work.json',
                              '--template', 'example/address-book.mako',
                              '--output', 'tests/address-book.html'])
