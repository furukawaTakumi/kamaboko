# 否定型の考慮
# 並列関係への対応
import os, glob, MeCab, json


import kamaboko
from .PolalityDict import PolalityDict


class Kamaboko:
    def __init__(self) -> None:
        self.dictionary = PolalityDict()
        self.tokenizer = MeCab.Tagger().parseToNode

    def analyze(self, text):
        node = self.tokenizer(text)
        tokens = self.__conv_to_standard_form(node)
        result = self.__count_polality(tokens)
        return result

    def __count_polality(self, tokens: list):
        positive_num, negative_num = 0, 0
        tmp_dict = self.dictionary
        for tkn in tokens:
            if not tkn in tmp_dict.keys():
                tmp_dict = self.dictionary
                continue

            if tmp_dict[tkn]['is_end']:
                positive_num += tmp_dict[tkn]['polality'] == 'p'
                negative_num += tmp_dict[tkn]['polality'] == 'n'
                tmp_dict = self.dictionary
            else:
                tmp_dict = self.dictionary[tkn]
        return positive_num, negative_num
    
    def __conv_to_standard_form(self, node):
        tokens = []
        while node:
            standard_form = node.feature.split(',')[6] # standard form exists on index 6
            tokens.append(standard_form)
            node = node.next
        return tokens[1:-1] # token of index 0 and -1 is '*'



