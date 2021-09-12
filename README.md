# kamaboko: A sentimental analysis library with user-modifiable dictionaries
ユーザが変更可能な辞書を持つシンプルな感情分析ライブラリです．  
快不快を判定します．

**特徴**
- 感情極性辞書を柔軟にインストール可能
- 不快語彙の否定を快としないこと

CSVまたはTSV形式で作成された感情極性辞書を柔軟にインストールすることができます．

# Requirements
あらかじめインストールする必要があるライブラリは以下の通りです．

- MeCab
- CaboCha

# 使い方
使用する前に**感情極性辞書をインストール**する必要があります．  
辞書のインストールは「極性辞書の設置」の項を参照してください．  

※以降のサンプルプログラムの出力は[日本語評価極性辞書](https://www.cl.ecei.tohoku.ac.jp/Open_Resources-Japanese_Sentiment_Polarity_Dictionary.html)(名詞編と用言編)をkamabokoにインストールした場合のものです．
```python
import kamaboko

analyzer = kamaboko.Kamaboko()
result = analyzer.analyze('こんにちは．今日はいい天気で気分がいいです．')
print(result)
```
**output**
```sh
{'positive': 1.0, 'negative': 0.0}
```

結果は辞書形式で各極性である可能性が0~1の範囲で示されます．  
  
`analyzed_sequence`を用いれば，解析結果の内容を見ることもできます．

```
from pprint import pprint
result = analyzer.analyzed_sequence('こんにちは．今日はいい天気で気分がいいです．')
```
**output**
```py
[{'belong_to': 0,
  'chunk_to': 5,
  'conjugation': '*',
  'conjugation_form': '*',
  'pos': '感動詞',
  'pos_detail_1': '*',
  'pos_detail_2': '*',
  'pos_detail_3': '*',
  'pronunciation': 'コンニチワ',
  'reading': 'コンニチハ',
  'standard_form': 'こんにちは',
  'surface': 'こんにちは'},
  
  ~~~ 省略 ~~~

 {'belong_to': 5,
  'conjugation': '*',
  'conjugation_form': '*',
  'is_scaned': True,
  'pos': '記号',
  'pos_detail_1': '句点',
  'pos_detail_2': '*',
  'pos_detail_3': '*',
  'pronunciation': '．',
  'reading': '．',
  'standard_form': '．',
  'surface': '．'}]
```
項目の詳細は`src/kamaboko/analyzers/CaboChaAnalyzer.py`を参照してください．  
なお，動的に追加される基本的な属性には以下のものがあります．  
- polality
  - 形態素の極性を表現
- negation_count
  - その形態素が否定された回数

## 極性辞書のインストール
感情分析を行う前に辞書をインストールする必要があります．  
辞書インストールのコマンドは`install_dictionary`です．  
`install_dictionary -h`でヘルプが出ます．  

基本的な使い方は以下の通りです．
```
install_dictionary path/to/dictionary_file dictionary_type
```

`dictionary_type`にはnounかcollocationを指定します．なお，現時点で実行時の違いはありません．ご了承ください．

あとはオプションとなっています．

- `--file_format`  
  ファイルの形式を指定します．指定できるのは`csv`か`tsv`です．`-ff`がショートカットです．
- `--word_idx`  
  語彙のカラム番号です．指定により，**どのカラム列に語彙が記載されていても**読み込めます．`-wi`がショートカットです．
- `--polality_idx`  
  極性のカラム番号です．指定により，**どのカラムに極性ラベルが記載されていても**読み込めます．`-pi`がショートカットです．
- `--positive_labels`  
  ポジティブラベルを指定します．複数指定可能です．指定にしたラベルのいずれかに一致した場合にその語彙をポジティブ語彙とします．`-pl`がショートカットです．
- `--negative_labels`  
  ネガティブラベルを指定します．複数指定可能です．指定にしたラベルのいずれかに一致した場合にその語彙をネガティブ語彙とします．`-nl`がショートカットです．


### インストール例
以下は[日本語評価極性辞書](https://www.cl.ecei.tohoku.ac.jp/Open_Resources-Japanese_Sentiment_Polarity_Dictionary.html)をインストールする例です．

**用言編**
```sh
install_dictionary path/to/wago.121808.pn collocation -ff tsv -pi 0 -wi 1 -pl ポジ（評価） -pl ポジ（経験） -nl ネガ（経験） -nl ネガ（評価）
```

**名詞編**
```sh
install_dictionary path/to/pn.csv.m3.120408.trim noun -ff tsv -pi 1 -wi 0
```

## インストールした辞書を確認する
以下のコマンドでインストールした辞書を閲覧できます．
```
list_dictionary
```

**結果**
```
resource
    collocation
        wago.121808.pn
    noun
        pn.csv.m3.120408.trim
```
kamabokoは`collocation`ディレクトリと`noun`ディレクトリの中に辞書を保存しますが，現時点(2021/9/12)で実質的な違いはありません．

## 極性辞書を削除する
以下のコマンドで極性辞書を削除します．
```
delete_dictionary DIC_TYPE DIC_NAME
```
`DIC_TYPE`には`noun`または`collocation`のいずれかが入ります．
`DIC_NAME`は感情極性辞書の名前です．

例えば，`collocation`ディレクトリに入っている`wago.121808.pn`を削除したい場合には，以下のコマンドを実行します．
```sh
delete_dictionary collocation wago.121808.pn
```
# ライセンス
MIT License

Copyright (c) 2021 furukawaTakumi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# 引用について
本ライブラリについて言及する場合におきましては，以下を引用ください．  

`古川,菱田 ユーザが変更可能な辞書を持つ感情分析ライブラリ, 電気・電子・情報関係学会東海支部連合大会, 2021, H6-5`

# 謝辞
本研究の一部は，JSPS 科研費 JP19K12073 の助成を受けたものです.