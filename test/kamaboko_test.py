

import unittest
from  collections.abc import Mapping


from kamaboko import Kamaboko

class KamabokoTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_instance(self):
        kamaboko = Kamaboko()
        self.assertIsInstance(kamaboko, Kamaboko)

    def tearDown(self):
        pass