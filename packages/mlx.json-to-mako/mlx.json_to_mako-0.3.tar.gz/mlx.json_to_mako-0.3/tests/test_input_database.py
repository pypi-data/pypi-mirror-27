from unittest import TestCase
from mlx.json_to_mako import InputDatabase


class TestInputDatabase(TestCase):

    def test_ok(self):
        db = InputDatabase('example/family.json')
        self.assertEqual('example/family.json', db.source)
        self.assertEqual('family', db.name)
        self.assertIsNotNone(db.data)
