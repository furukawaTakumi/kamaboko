# 否定型の考慮
# 並列関係への対応
import os, glob, json


import kamaboko
from .PolalityDict import PolalityDict


class Kamaboko:
    def __init__(self, tokenizer) -> None:
        self.dictionary = PolalityDict()
        self.tokenizer = tokenizer

    def analyze(self, text):
        tokens = self.tokenizer(text)
        result = self.__count_polality(tokens)
        return result

    def __count_polality(self, tokens: list):
        positive_num, negative_num = 0, 0
        tmp_dict = self.dictionary
        for tkn in tokens:
            st_form = tkn['standard_form']
            if not st_form in tmp_dict.keys():
                tmp_dict = self.dictionary
                continue

            if tmp_dict[st_form]['is_end']:
                positive_num += tmp_dict[st_form]['polality'] == 'p'
                negative_num += tmp_dict[st_form]['polality'] == 'n'
                tmp_dict = self.dictionary
            else:
                tmp_dict = tmp_dict[st_form]
        return positive_num, negative_num
