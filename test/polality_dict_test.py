import os, sys
import unittest

from attrdict.mixins import Attr


from kamaboko.PolalityDict import PolalityDict
from cli import install, delete as delete_dic
from attrdict import AttrDict

class PolalityDictTest(unittest.TestCase):
    @staticmethod
    def setUpClass():
        install_opt = AttrDict({
            "dic_path": "./test/test_resource/sample_noun_dict.txt",
            "dic_type": "noun",
            "file_format": "csv",
            "word_idx": 0,
            "polality_idx": 1,
            "positive_labels": ['p'],
            "negative_labels": ['n']
        })
        install(install_opt)
        pass

    def setUp(self) -> None:
        self.dictionary = PolalityDict()

    def test_dict_like(self):
        self.assertIsInstance(self.dictionary, PolalityDict)

        for key in self.dictionary.keys():
            self.assertIsInstance(self.dictionary[key], str)

    def test_custumize(self):
        self.assertEqual(self.dictionary['ゴールドシップ'], 'p')
        self.assertEqual(self.dictionary['ありがた迷惑'], 'p', "書き換えができていないようです")

    @staticmethod
    def tearDownClass():
        delete_opt = AttrDict()
        delete_opt.dic_type = "noun"
        delete_opt.dic_name = "sample_noun_dict.txt"
        delete_dic(delete_opt)
        pass