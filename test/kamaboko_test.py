

import unittest
from  collections.abc import Mapping


from kamaboko import Kamaboko
from kamaboko.tokenizers import MecabTokenizer

# 日本語評価極性辞書（用言編）・日本語評価極性辞書（名詞編）を用いた場合のテスト

class KamabokoTest(unittest.TestCase):
    def setUp(self):
        tokenize = MecabTokenizer()
        self.kamaboko = Kamaboko(tokenize)
        pass

    def test_analyze(self):
        result = self.kamaboko.analyze("""
        日本にいた頃は一日中、毎晩深夜遅くまで働いていたせいで、美容とかおしゃれとかに縁遠く、立派な喪女だったけど、あまりの変化に最近では鏡を見るのがちょっと楽しい。
        """)
        self.assertEqual((3,1), result) # osetiではpositiveが3, negativeが1である
    
    def test_negative_collocation(self):
        result = self.kamaboko.analyze("""途方も無い作業だ．""")
        self.assertEqual((0,1), result)

        # TODO: 「途方もない」だとマッチしない．
        # データには存在しているので辞書インストール時のバグであると考えられる

    # def test_react_negative(self):
    #     result = self.kamaboko.analyze("""
    #     それでは加賀が救われない．
    #     """) # ポジティブ動詞　＋　動詞（未然形）　＋　助動詞（ない）　＝　ネガティブ
    #     self.assertEqual((0, 1), result)

    #     result = self.kamaboko.analyze("""
    #     わかった、怒らないから、はなしてごらん？
    #     """) # ポジティブ動詞（未然形）　＋　助動詞（ない）　＝　ネガティブ
    #     self.assertEqual((0, 1), result)

    def tearDown(self):
        pass