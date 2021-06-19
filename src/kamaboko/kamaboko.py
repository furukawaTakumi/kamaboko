# 否定型の考慮
# 並列関係への対応
import os, glob, json
from pprint import pprint

import kamaboko
from .PolalityDict import PolalityDict
from .analyzers import CaboChaAnalyzer


class Kamaboko:
    def __init__(self, tokenizer) -> None:
        self.dictionary = PolalityDict()
        self.cabocha = CaboChaAnalyzer()
        if tokenizer is not None:
            self.tokenizer = tokenizer

    def analyze(self, text):
        tokens, chunks = self.cabocha(text)
        tokens = self.__apply_polality_word(tokens)
        self.__apply_negation_word(tokens, chunks)
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
                if 0 < depth:
                    for i in range(idx - depth, idx + 1):
                        tokens[i]['is_collocation_parts'] = True
                    tokens[idx - depth]['is_collocation_start'] = True
                    tokens[idx]['is_collocation_end'] = True
                    tokens[idx - depth].polality = self.__calc_score(tmp_dict[st_form]['polality'])
                else:
                    tokens[idx].polality = self.__calc_score(tmp_dict[st_form]['polality'])

                tmp_dict = self.dictionary
                depth = 0
            else:
                tmp_dict = tmp_dict[st_form]
                depth += 1
        return tokens
    
    def __apply_negation_word(self, tokens, chunks):
        for c_idx, chunk in enumerate(chunks):
            for tkn in chunk:
                if not 'polality' in tkn.keys():
                    continue
                print('tkn', tkn.standard_form)
                chunk_items = self.__collect_dep_chunks(c_idx, chunks)
                print('chunk_items', chunk_items)
                negation_count = self.__negation_count(chunk_items)
                print('negation_count', negation_count)

                tkn.polality = tkn.polality * pow(-1, negation_count)
    
    def __collect_dep_chunks(self, start: int, chunks):
        chunk_items = []
        to = start
        
        while True:
            chunk = chunks[to]
            chunk_items.extend(chunk)
            to = chunk[0].chunk_to

            if to == -1:
                break
        return chunk_items

    def __negation_count(self, chunk_items):
        negation_cnt = 0
        for idx, c in enumerate(chunk_items):
            print('c.standard_form', c.standard_form)
            if idx + 1 < len(chunk_items) \
            and '接続助詞' == c.pos_detail_1 \
            and chunk_items[idx + 1].pos_detail_1 == '自立':
                break
            if not 'is_collocation_parts' in c.keys() \
            and c.standard_form in self.dictionary.NEGATION_WORDS:
                negation_cnt += 1
        return negation_cnt

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
