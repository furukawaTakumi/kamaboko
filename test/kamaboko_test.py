

import unittest
from  collections.abc import Mapping


from kamaboko import Kamaboko

# 日本語評価極性辞書（用言編）・日本語評価極性辞書（名詞編）を用いた場合のテスト

class KamabokoTest(unittest.TestCase):
    def setUp(self):
        self.kamaboko = Kamaboko()
        pass

    def test_analyze(self):
        result = self.kamaboko.analyze("""
        日本にいた頃は一日中、毎晩深夜遅くまで働いていたせいで、美容とかおしゃれとかに縁遠く、立派な喪女だったけど、あまりの変化に最近では鏡を見るのがちょっと楽しい。
        """)
        self.assertEqual((3,1), result) # osetiではpositiveが3, negativeが1である

    def tearDown(self):
        pass