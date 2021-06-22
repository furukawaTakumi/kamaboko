
import re

from .PolalityDict import PolalityDict
from .analyzers import CaboChaAnalyzer


class Kamaboko:
    def __init__(self) -> None:
        self.dictionary = PolalityDict()
        self.cabocha = CaboChaAnalyzer()

    def analyze(self, text):
        tokens, chunks = self.cabocha(text)
        self.__apply_polality_word(tokens)
        self.__mark_subject(tokens, chunks)
        self.__mark_parallel(tokens)
        self.__apply_negation_word(tokens, chunks)
        # print('tokens', tokens)
        result = self.__count_polality(tokens)
        return result

    def __apply_polality_word(self, tokens: list):
        for idx, _ in enumerate(tokens):
            key_items = []
            for sub_tkn in tokens[idx:]:
                key_items.append(sub_tkn.standard_form)
                key = ' '.join(key_items)
                if key in self.dictionary.keys():
                    tokens[idx].polality = self.__calc_score(self.dictionary[key]) # 連語を優先 (単語の極性値は連語の極性値で上書き)
                    
                    if len(key_items) > 1:
                        for j in range(len(key_items)):
                            tokens[idx + j].is_collocation_parts = True
    
    def __apply_negation_word(self, tokens, chunks):
        for tkn in tokens: # 主辞を優先して探索
            if 'is_subject' in tkn.keys() or 'is_parallel_parts' in tkn.keys():
                chunk = chunks[tkn.belong_to]
                for c in chunk:
                    if not 'polality' in c.keys():
                        continue
                    chunk_items = self.__collect_dep_chunks(c.belong_to, chunks)
                    negation_count = self.__negation_count(chunk_items, False)
                    c.polality *= pow(-1, negation_count)

        for c_idx, chunk in enumerate(chunks):
            for tkn in chunk:
                if not 'polality' in tkn.keys():
                    continue
                chunk_items = self.__collect_dep_chunks(c_idx, chunks)
                negation_count = self.__negation_count(chunk_items)
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

    def __negation_count(self, chunk_items, apply_scaned=True):
        negation_cnt = 0
        for idx, c in enumerate(chunk_items):
            if idx + 1 < len(chunk_items) \
            and '接続助詞' == c.pos_detail_1 \
            and chunk_items[idx + 1].pos_detail_1 == '自立':
                break
            if apply_scaned and 'is_scaned' in chunk_items[idx].keys():
                break
            if not 'is_collocation_parts' in c.keys() \
            and c.standard_form in self.dictionary.NEGATION_WORDS:
                c.is_scaned = True
                negation_cnt += 1
        return negation_cnt

    def __mark_subject(self, tokens, chunks):
        for idx in range(0, len(tokens) - 1):
            if tokens[idx].pos != '名詞':
                continue
            
            tmp_idx = idx
            if tokens[idx+1].pos == '名詞' \
            and tokens[idx+1].pos_detail_1 == '接尾':
                tmp_idx + 1
            if tokens[tmp_idx+1].pos_detail_1 == '格助詞' \
            and tokens[tmp_idx+1].standard_form == 'が':
                tokens[idx].is_subject = True
            if tokens[tmp_idx+1].pos_detail_1 == '係助詞' \
            and tokens[tmp_idx+1].standard_form == 'は':
                tokens[idx].is_subject = True
            
            if 'is_subject' in tokens[idx].keys():
                if '非自立' == tokens[idx].pos_detail_1: # わけ[非自立]がない　などに対応
                    chunks[tokens[idx].belong_to - 1][0].is_subject = True
                elif tokens[idx].pos == '名詞':
                    tokens[idx].is_subject = True
    
    def __mark_parallel(self, tokens):
        regex = re.compile("名詞(と|や|も|やら|に)名詞")

        for base_idx in range(len(tokens)):
            target = ''
            depth = 0
            for tkn in tokens[base_idx:]:
                if '名詞' == tkn.pos:
                    target += '名詞'
                else:
                    target += tkn.standard_form
                depth += 1
                if regex.fullmatch(target):
                    for i in range(base_idx, base_idx+depth):
                        tokens[i].is_parallel_parts = True
                    break

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
