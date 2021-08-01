
import re

from .PolalityDict import PolalityDict
from .analyzers import CaboChaAnalyzer
from .DisplayFilter import DisplayFilter
from .Rules import Rules


class Kamaboko:
    def __init__(self, display_filter: DisplayFilter = None) -> None:
        self.dictionary = PolalityDict()
        self.cabocha = CaboChaAnalyzer()
        if display_filter is None:
            self.display_filter = DisplayFilter()
        else:
            self.display_filter = display_filter

    def analyze(self, text):
        tokens = self.__analyze(text)
        positive, negative = self.__count_polality(tokens)
        all_cnt = positive + negative
        if all_cnt == 0:
            return { "positive": 0.5, "negative": 0.5 }
        else:
            return {
                "positive": positive / all_cnt,
                "negative": negative / all_cnt
            }

    def analyzed_sequence(self, text):
        tokens = self.__analyze(text)
        return self.display_filter.done(tokens)

    def count_polality(self, text):
        tokens = self.__analyze(text)
        return self.__count_polality(tokens)

    def __analyze(self, text):
        tokens, chunks = self.cabocha(text)
        self.__apply_polality_word(tokens)
        self.__mark_subject(tokens, chunks)
        self.__mark_parallel(tokens)
        self.__mark_tigainai(chunks)
        self.__mark_kamosirenai(chunks)
        self.__apply_negation_word(tokens, chunks)
        return tokens

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
            if 'is_subject' in tkn.keys():
                chunk = chunks[tkn.belong_to]
                for c in chunk:
                    if not 'polality' in c.keys():
                        continue
                    chunk_items = self.__collect_dep_chunks(c.belong_to, chunks)
                    negation_count = self.__negation_count(chunk_items, False)
                    c.negation_count = negation_count
                    c.polality *= pow(-1, negation_count)

        for c_idx, chunk in enumerate(chunks):
            for tkn in chunk:
                if not 'polality' in tkn.keys() or 'is_scaned' in tkn.keys():
                    continue
                chunk_items = self.__collect_dep_chunks(c_idx, chunks)
                negation_count = self.__negation_count(chunk_items)
                tkn.negation_count = negation_count
                tkn.polality = tkn.polality * pow(-1, negation_count)

        parallel_parts_items = self.__collect_parallel_parts(tokens)

        for parts in parallel_parts_items:
            for tkn in parts:
                if 'negation_count' in tkn.keys() and tkn.negation_count:
                    parts.append(tkn.negation_count)
                    break

        for parts in parallel_parts_items:
            if not isinstance(parts[-1], int):
                continue
            v = parts.pop()
            for tkn in parts:
                if not 'negation_count' in tkn.keys() or tkn.negation_count == 0:
                    tkn.negation_count = v
                    tkn.polality *= pow(-1, v)

    def __collect_parallel_parts(self, tokens):
        parallel_parts = []
        tmp_parts = []
        for tkn in tokens:
            if 'is_parallel_parts' in tkn.keys() \
            and 'polality' in tkn.keys():
                tmp_parts.append(tkn)
                if 'is_parallel_end' in tkn.keys():
                    parallel_parts.append(tmp_parts)
                    tmp_parts = []
        return parallel_parts
    
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

        for idx, tkn in enumerate(chunk_items):
            if idx + 1 < len(chunk_items) \
            and '接続助詞' == tkn.pos_detail_1 \
            and chunk_items[idx + 1].pos_detail_1 == '自立':
                break
            if apply_scaned and 'is_scaned' in chunk_items[idx].keys():
                break
            if \
            not 'is_collocation_parts' in tkn.keys() \
            and not 'is_tigainai' in tkn.keys() \
            and not 'is_kamosirenai' in tkn.keys() \
            and self.dictionary.is_negation(tkn):
                negation_cnt += 1
            tkn.is_scaned = True
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
        regex = re.compile("n((p)n)+")
        target = ''
        for base_idx in range(len(tokens)):
            if '名詞' == tokens[base_idx].pos:
                target += 'n'
            elif tokens[base_idx].standard_form in ['と', 'や', 'も', 'に' ,'や' ,'ら']:
                target += 'p'
            else:
                target += 'e'
        for m in regex.finditer(target):
            for idx in range(m.start(), m.end()):
                tokens[idx].is_parallel_parts = True
            tokens[m.start()].is_parallel_start = True
            tokens[m.end() - 1].is_parallel_end = True

    def __mark_tigainai(self, chunks):
        for chunk in chunks:
            if Rules.is_tigainai(chunk):
                for token in chunk:
                    token.is_tigainai = True

    def __mark_kamosirenai(self, chunks):
        for chunk in chunks:
            if Rules.is_kamosirenai(chunk):
                for token in chunk:
                    token.is_kamosirenai = True

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
