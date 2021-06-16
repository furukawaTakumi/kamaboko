

import unittest


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
    
    def test_collocation(self):
        result = self.kamaboko.analyze("""途方も無い作業だ．""")
        self.assertEqual((0,1), result, "前方一致している連語に対処できていないようです")

        result = self.kamaboko.analyze("""途方もない作業だ．""")
        self.assertEqual((0,1), result, "前方一致している連語に対処できていないようです")

        result = self.kamaboko.analyze("""え、まったく違和感ないわ""")
        self.assertEqual((1,0), result, "前方一致している連語に対処できていないようです")
        result = self.kamaboko.analyze("""まったく違和感がないです．""")
        self.assertEqual((1,0), result, "前方一致している連語に対処できていないようです")

    def test_collocation_negation(self):
        result = self.kamaboko.analyze("""
        この靴のサイズ、ふたつとなくない？
        """) # ふたつとないがポジティブで、その否定だから
        self.assertEqual((0, 1), result)

    def test_react_negation(self):
        result = self.kamaboko.analyze("""
        それでは加賀が救われない．
        """) # ポジティブ動詞　＋　動詞（未然形）　＋　助動詞（ない）　＝　ネガティブ
        self.assertEqual((0, 1), result)

        result = self.kamaboko.analyze("""
        わかった、怒らないから、はなしてごらん？
        """) # ポジティブ動詞（未然形）　＋　助動詞（ない）　＝　ネガティブ
        self.assertEqual((1, 0), result, '"怒る-ない"に無反応です')

        result = self.kamaboko.analyze("""
        死ななかろう
        """)
        self.assertEqual((1, 0), result, '"死な-ない"に無反応です')

        result = self.kamaboko.analyze("""
        そんなこと、信じられない！
        """)
        self.assertEqual((0, 1), result, '"信じる-られる-ない"に無反応です')

        result = self.kamaboko.analyze("""
        信じられぬから信じぬぞ！
        """)
        self.assertEqual((0, 2), result, '"信じる-られる-ぬ","信じる-ぬ"に無反応です')

        result = self.kamaboko.analyze("""
        馬鹿な．信じられるわけがないだろう
        """)
        self.assertEqual((0, 1), result, '"信じられるわけが-ない"に無反応です')

    def test_arimasen_negation(self):
        result = self.kamaboko.analyze("""
        このラーメンは美味しくありません．
        """)
        self.assertEqual((0, 1), result, '"ある-ます-ん"に反応していません')

    def test_postpositional_particle(self):
        result = self.kamaboko.analyze("""
        利点がない
        """)
        self.assertEqual((0, 1), result)

    def test_not_exist_word_negation(self):
        result = self.kamaboko.analyze("""お金がないうえアダマンタイトもない""") # アダマンタイトは未登録語彙
        self.assertEqual((0, 1), result, "未登録語彙アダマンタイトの否定により解析が失敗")

    # def test_triple_negation(self):
        # text = "人望も金も技術も、ない人間が、ただ一人運命に抗う物語"
        # 人望 金 技術 => + 3, ないないづくし 
        # result = self.kamaboko.analyze(text)
        # self.assertEqual((0, 3), result, "")




    def tearDown(self):
        pass