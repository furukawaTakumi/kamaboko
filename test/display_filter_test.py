import unittest
import sys, os

from kamaboko import Kamaboko, DisplayFilter

class DisplayFilterTest(unittest.TestCase):
    def setUp(self):
        self.kamaboko = Kamaboko()
        pass

    def test_done(self):
        tokens = self.kamaboko.analyzed_sequence("""
        日本にいた頃は一日中、毎晩深夜遅くまで働いていたせいで、美容とかおしゃれとかに縁遠く、立派な喪女だったけど、あまりの変化に最近では鏡を見るのがちょっと楽しい。
        """)
        keys = {'surface', 'polality', 'negation_count'}
        f = DisplayFilter(keys)
        result = f.done(tokens)
        self.assertLess(0, len(result))
        for t in result:
            self.assertLessEqual(len(t.keys()), 3, f"{t}")

    def test_display_warning(self):
        filename = 'text_tmp.txt'
        keys = {'asdf', '39348584347'} # not found keys
        with open(filename, 'w') as io:
            sys.stdout = io
            DisplayFilter(keys)
        sys.stdout = sys.__stdout__

        with open(filename, 'r') as io:
            self.assertEqual(2, io.read().count('Warning'), 'display warning not working')

        os.remove(filename)


    def tearDown(self):
        pass