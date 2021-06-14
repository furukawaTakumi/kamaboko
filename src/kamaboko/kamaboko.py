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
        print('tokens', tokens)
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
            if not 'polality' in tkn.keys():
                continue
            tkn['negation_count'] = 0
            if not tkn['pos'] in ['形容詞', '動詞']:
                continue

            for t in tokens[idx+1:min(idx+4,len(tokens))]:
                if not t['pos'] in ['動詞', '助動詞']:
                    break
                if t['pos'] == '助動詞' and t['standard_form'] in self.dictionary.NEGATION_WORDS:
                    tkn['polality'] *= -1
                    tkn['negation_count'] += 1
                    t['is_negation_word'] = True
                    break

                if t['conjugation'] != '未然形': # （助）動詞の未然形に否定語は繋がってくる 待た せ ない　など来た時のために動詞もokに
                    break
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
