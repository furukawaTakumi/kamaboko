# 否定型の考慮
# 並列関係への対応
import os, glob, json
from pprint import pprint

import kamaboko
from .PolalityDict import PolalityDict
from .tokenizers import MecabTokenizer


class Kamaboko:
    def __init__(self, tokenizer) -> None:
        self.dictionary = PolalityDict()
        self.tokenizer = MecabTokenizer()
        if tokenizer is not None:
            self.tokenizer = tokenizer

    def analyze(self, text):
        tokens = self.tokenizer(text)
        tokens = self.__apply_polality_word(tokens)
        tokens = self.__apply_negation_word(tokens)
        # tokens = self.__apply_arimasen(tokens)
        result = self.__count_polality(tokens)
        return result

    def __apply_polality_word(self, tokens: list):
        tmp_dict = self.dictionary
        depth = 0
        for idx, tkn in enumerate(tokens):
            st_form = tkn['standard_form']
            if not st_form in tmp_dict.keys():
                tmp_dict = self.dictionary
                depth = 0
                continue

            if tmp_dict[st_form]['is_end']:
                tokens[idx]['polality'] = self.__calc_score(tmp_dict[st_form]['polality'])

                if 0 < depth:
                    for i in range(idx - depth, idx + 1):
                        tokens[i]['is_collocation_parts'] = True
                    tokens[idx - depth]['is_collocation_start'] = True
                    tokens[idx]['is_collocation_end'] = True

                tmp_dict = self.dictionary
                depth = 0
            else:
                tmp_dict = tmp_dict[st_form]
                depth += 1
        return tokens

    def __apply_negation_word(self, tokens: list):
        for idx, tkn in enumerate(tokens):
            for i in range(1, len(tokens)):
                if idx + i >= len(tokens):
                    break
                if 'polality' in tokens[idx + i]:
                    break
                if '接続詞' == tokens[idx + 1]['pos']:
                    break # 接続詞が入るところで一つの意味となるので
                if tokens[idx + i]['standard_form'] in self.dictionary.NEGATION_WORDS:
                    tokens[idx]['negation_count'] + 1
                    tokens[idx]['polality'] *= -1
        return tokens
    
    def __apply_subject_predicate(self, tokens: list):
        # 主述関係の把握 nsubj
        # 述語を修飾するものをあげていき、そこに否定語が含まれているかをチェック．
        return tokens

    def __calc_score(self, polality: str):
        if polality == 'p':
            return 1
        elif polality == 'n':
            return -1
        else:
            return 0

    def __count_polality(self, tokens: list):
        positive_num, negative_num = 0, 0
        for tkn in tokens:
            if not 'polality' in tkn.keys():
                continue
            if 0 < tkn['polality']:
                positive_num += 1
            elif 0 > tkn['polality']:
                negative_num += 1
        return positive_num, negative_num
