

import unittest
from unittest.case import SkipTest


from kamaboko import Kamaboko
import kamaboko

# 日本語評価極性辞書（用言編）・日本語評価極性辞書（名詞編）を用いた場合のテスト

class KamabokoTest(unittest.TestCase):
    def setUp(self):
        f = kamaboko.DisplayFilter({'standard_form', 'polality', 'negation_count'})
        self.kamaboko = Kamaboko(f)
        pass

    def evaluate(self, text, excepted):
        result = self.kamaboko.count_polality(text)
        self.assertEqual(excepted, result, text)
    
    def evaluate_percentage(self, text, positive_percent, negative_percent):
        result = self.kamaboko.analyze(text)
        self.assertAlmostEqual(1, positive_percent + negative_percent, "合計が1になりません．\ninput: f{text}")
        self.assertAlmostEqual(result["positive"], positive_percent)
        self.assertAlmostEqual(result["negative"], negative_percent)

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

    def test_looks_like_not_is_not_not(self):
        self.evaluate("つまり、レベルアップしたことで、スキルの熟練度にボーナスポイントが加算されたんだ！", (5, 0))
        self.evaluate("だから一気に２個もスキルレベルが上がったんだ。", (1, 0))
        self.evaluate("洞窟っていう地形もナイスだと思うんですよ。", (1, 0))
        self.evaluate("初めてだからきっと失敗しちゃったんだよ。", (0,1))
        self.evaluate("なんて無駄使いを私はしてしまったんだ！", (0, 1))
        self.evaluate("まして私は前世では学校に通うだけで、息切れするようなもやしっ子だったんだし。", (0, 1))
        self.evaluate("マイホームの外は魔物の脅威で溢れているんだから。", (0, 1))
    
    def test_kamosirenai(self):
        self.evaluate("そうすれば，利益が出たかもしれない", (1,0)) # 連語をまとめて判断する
        pass

    def test_tigainai(self):
        self.evaluate("きっとこの石が情報の価値もない、本当にただの石ころだからに違いない！", (1, 1))
        self.evaluate("この世界では貝殻はお金に違いない！", (1, 0))
        pass

    @unittest.skip('no implement')
    def test_sinakyanaranai(self):
        # self.evaluate("一度痛い思いをしなきゃならないけど、それを我慢すれば、耐性を得ることができる。", (1, 2)) # しなきゃならないはないが二つでていずれにせよ2回否定して極性が戻るのでやらなくても良いかも
        pass

    @unittest.skip('no implement')
    def test_punctuation_cat(self):
        self.evaluate("まあ、耐性があるおかげか、我慢できなくはない。", (1, 0)) # 
        self.evaluate("本当は素早さだけじゃなくて、その他の運動能力も軒並み前世より高いです、はい。", (2, 0)) # だけでなく他も高い
        self.evaluate("お金が欲しいといっているわけではなくて") # 誤解を解く
        self.evaluate("他にどんなスキルがあったのかはわからないけど、もしかしたらＬＶ１でももっと使えるスキルがあったかもしれないのに！", (0, -2))
        pass

    @unittest.skip('no implement')
    def test_todo(self): # TODO
        self.evaluate("つまり、ＬＶ１ではほとんど役に立たない効果しか発揮してくれないってことなんでしょ。", (1, 2)) # 否定箇所バグ
        self.evaluate("情報が少なすぎてわからないことが多すぎる。", (0, -1)) # 否定み適用バグ
        self.evaluate("まっとうな人生なんて送れないだろうし、あ、そもそも蜘蛛だから人生じゃなくて蜘蛛生か。", (0, 2)) # 蜘蛛が否定されてしまう
        self.evaluate("体は魔物でも、それを動かす中身がしょっぱければ意味ないし。", (1, 2)) # 意味　が否定されない
        self.evaluate("野生の本能で生きてる本物の魔物相手に、戦って勝てるかというと、難しいんじゃないかと思う。", (2, 1))
        self.evaluate("新しく新居を作るにも体力を消耗するし、何よりもいい条件の立地を探さなければならない。", (1, 0)) 
        self.evaluate("鑑定でこんなざまなら、他のスキルもきっとＬＶ１じゃどうしようもない効果しか出なかったんだと。", (1,1))
        self.evaluate("細いと脆くなって、太いと頑丈になるのは確認したけど、じゃあ、どこまでの力に耐えられるのかというのは、残念ながらわからなかった。", )


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

    # def test_other_negation(self): # TODO
    #     self.evaluate("利点しかない", (1, 0))

    def test_percentage(self):
        self.evaluate_percentage("""利点はある""", 1, 0)
        self.evaluate_percentage("企業は損失を被った", 0, 1)
        self.evaluate_percentage("""電話にでんわ！""", 0.5, 0.5) # 何もマッチしないとき
        self.evaluate_percentage("""利益は今週末に間違いなく洞窟に入ったところに置いておくと言われていたのに払われていない．""", 0.5, 0.5) # polalityの数が 1 : 1
        self.evaluate_percentage("""
        日本にいた頃は一日中、毎晩深夜遅くまで働いていたせいで、美容とかおしゃれとかに縁遠く、立派な喪女だったけど、あまりの変化に最近では鏡を見るのがちょっと楽しい。
        """, 0.75, 0.25)
        
