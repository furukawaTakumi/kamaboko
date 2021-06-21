import unittest


from kamaboko.PolalityDict import PolalityDict

class PolalityDictTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_dict_like(self):
        dic = PolalityDict()
        self.assertIsInstance(dic, PolalityDict)

        for key in dic.keys():
            self.assertIsInstance(dic[key], str)


    def tearDown(self):
        pass