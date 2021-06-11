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
        root = self.tokenizer(text)
        tokens = self.__conv_to_dic_format(root)
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
    
    def __conv_to_dic_format(self, node):
        tokens = []
        while node:
            features = node.feature.split(',')
            token_feature = {
                'surface': node.surface,
                'pos': features[0],
                'pos_detail-1': features[1],
                'pos_detail-2': features[2],
                'pos_detail-3': features[3],
                'conjugation-form': features[4],
                'conjugation': features[5],
                'standard_form': features[6],
                'reading': features[7],
                'pronunciation': features[8]
            }
            tokens.append(token_feature)
            node = node.next
        return tokens[1:-1] # token of index 0 and -1 is '*'



