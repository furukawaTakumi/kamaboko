

import unittest


from kamaboko import Kamaboko

# 日本語評価極性辞書（用言編）・日本語評価極性辞書（名詞編）を用いた場合のテスト

class KamabokoTest(unittest.TestCase):
    def setUp(self):
        self.kamaboko = Kamaboko()
        pass

    def evaluate(self, text, excepted):
        result = self.kamaboko.analyze(text)
        self.assertEqual(excepted, result, text)

    def test_analyze(self):
        self.evaluate("""
        日本にいた頃は一日中、毎晩深夜遅くまで働いていたせいで、美容とかおしゃれとかに縁遠く、立派な喪女だったけど、あまりの変化に最近では鏡を見るのがちょっと楽しい。
        """, (3, 1)) # osetiではpositiveが3, negativeが1である
    
    def test_collocation(self):
        self.evaluate("""途方も無い作業だ．""", (0, 1))
        self.evaluate("""途方もない作業だ．""", (0, 1))

    def test_collocation_negation(self):
        self.evaluate("""この靴のサイズ、ふたつとなくない？""", (0, 1))
        # ふたつとないがポジティブで、その否定だから

        self.evaluate("""え、まったく違和感ないわ""", (1, 0))
        self.evaluate("""まったく違和感がないです．""", (1, 0))

    def test_react_negation(self):
        self.evaluate("""それでは加賀が救われない．""", (0, 1)) # ポジティブ動詞　＋　動詞（未然形）　＋　助動詞（ない）　＝　ネガティブ
        self.evaluate("""わかった、怒らないから、はなしてごらん？""", (1, 0)) # ポジティブ動詞（未然形）　＋　助動詞（ない）　＝　ネガティブ
        self.evaluate("""死ななかろう""", (1, 0))
        self.evaluate("""そんなこと、信じられない！""", (0, 1))
        self.evaluate("""信じられぬから信じぬぞ！""", (0, 2))
        self.evaluate("""バカな、信じられるわけがないだろう""", (0, 2)) # バカ: -1, 信じられるわけがない: -1

    def test_arimasen_negation(self):
        self.evaluate("""このラーメンは美味しくありません．""", (0, 1))

    def test_postpositional_particle(self):
        self.evaluate("""利点がない""", (0, 1))
        self.evaluate("""利益は今週末に間違いなく洞窟に入ったところに置いておくと言われていたのに払われていない．""", (1, 1))
        self.evaluate("""今週末に間違いなく洞窟に入ったところに置いておくと言われていたのに利益分は払われていない．""", (1, 1))
        self.evaluate("""今週末に間違いなく利益分は洞窟に入ったところに置いておくと言われていたのに払われていない．""", (1, 1))

    def test_parallel_negation(self):
        self.evaluate("これは、人望とお金がない人間が、ただ一人運命に抗う物語", (0, 2)) # 人望 金 => +1 
        self.evaluate("人望もお金も学もない人間が、ただ一人運命に抗う物語", (0, 3))
        self.evaluate("人望とお金はあるけど、学はない人間が、ただ一人運命に抗う物語", (2, 1))

    def test_double_negation(self):
        self.evaluate("クラッカーは好きではないとは言わないが、それほどじゃない",(0, 1))
        self.evaluate("好ましいと思わないこともない", (1, 0))

    # def test_not_exist_word_negation(self):
    #     result = self.kamaboko.analyze("""お金がないうえにアダマンタイトもない""") # アダマンタイトは未登録語彙
    #     self.assertEqual((0, 1), result, "未登録語彙アダマンタイトの否定により解析が失敗")

    #     text = "不満はあるけど、いやではないかな" # 不満:-1, 「いや」は未登録語彙
    #     result = self.kamaboko.analyze(text)
    #     self.assertEqual((1, 1), result, text)

    def tearDown(self):
        pass