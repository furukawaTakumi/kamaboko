# 否定型の考慮
# 並列関係への対応
import os, glob, MeCab, json


import kamaboko
from .PolalityDict import PolalityDict


class Kamaboko:
    def __init__(self) -> None:
        self.dictionary = PolalityDict()
        self.tokenizer = MeCab.Tagger().parse

    def analyze(self, text):
        tokens = self.tokenizer(text)
        print('tokens', tokens)
        for t in tokens:
            print('t', t)
        return
