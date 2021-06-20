

import unittest


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
        self.assertEqual((3, 1), result) # osetiではpositiveが3, negativeが1である
    
    def test_collocation(self):
        text = """途方も無い作業だ．"""
        result = self.kamaboko.analyze(text)
        self.assertEqual((0,1), result, f"'{text}'に対処できていないようです")

        text = """途方もない作業だ．"""
        result = self.kamaboko.analyze(text)
        self.assertEqual((0,1), result, f"'{text}'に対処できていないようです")

        text = """え、まったく違和感ないわ"""
        result = self.kamaboko.analyze(text)
        self.assertEqual((1,0), result, f"'{text}'に対処できていないようです")

        text = """まったく違和感がないです．"""
        result = self.kamaboko.analyze(text)
        self.assertEqual((1,0), result, f"'{text}'に対処できていないようです")

    def test_collocation_negation(self):
        result = self.kamaboko.analyze("""
        この靴のサイズ、ふたつとなくない？
        """) # ふたつとないがポジティブで、その否定だから
        self.assertEqual((0, 1), result, "連語の否定が判定できていません")

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

        result = self.kamaboko.analyze("""
        利益は今週末に間違いなく洞窟に入ったところに置いておくと言われていたのに払われていない．
        """)
        self.assertEqual((1, 1), result, "〜がない、〜はない、に対応できていません")

        text = """
        今週末に間違いなく洞窟に入ったところに置いておくと言われていたのに利益分は払われていない．
        """
        result = self.kamaboko.analyze(text)
        self.assertEqual((1, 1), result, text)

        text = """
        今週末に間違いなく利益分は洞窟に入ったところに置いておくと言われていたのに払われていない．
        """
        result = self.kamaboko.analyze(text)
        self.assertEqual((1, 1), result, text)

    def test_not_exist_word_negation(self):
        result = self.kamaboko.analyze("""お金がないうえにアダマンタイトもない""") # アダマンタイトは未登録語彙
        self.assertEqual((0, 1), result, "未登録語彙アダマンタイトの否定により解析が失敗")

        # text = "不満はないけど、なんかいやだ"
        # result = self.kamaboko.analyze(text)
        # # TODO: 重複した語彙・連語による問題を解消する必要がある
        # self.assertEqual((1, 1), result, text)

    # def test_parallel_negation(self):
    #     text = "人望とお金がない人間が、ただ一人運命に抗う物語"
    #     # 人望 金 技術 => + 3, ないないづくし 
    #     result = self.kamaboko.analyze(text)
    #     self.assertEqual((0, 2), result, "")

    #     text = "人望もお金も学もない人間が、ただ一人運命に抗う物語"
    #     result = self.kamaboko.analyze(text)
    #     self.assertEqual((0, 3), result, "")

    def test_double_negation(self):
        text = "クラッカーは好きではないとは言わないが、それほどじゃない"
        result = self.kamaboko.analyze(text)
        self.assertEqual((0, 1), result)

        text = "好ましいと思わないこともない"
        result = self.kamaboko.analyze(text)
        self.assertEqual((1, 0), result)


    def tearDown(self):
        pass