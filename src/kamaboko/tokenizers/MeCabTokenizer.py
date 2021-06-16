
import MeCab
from collections import defaultdict

class MecabTokenizer:
    def __init__(self) -> None:
        self.mecab = MeCab.Tagger().parseToNode
        pass

    def __call__(self, text):
        node = self.mecab(text)
        return self.__conv_to_dic_format(node)

    def __conv_to_dic_format(self, node):
        tokens = []
        while node:
            features = node.feature.split(',')
            token_feature = defaultdict(lambda: 0, {
                'surface': node.surface,
                'pos': features[0],
                'pos_detail-1': features[1],
                'pos_detail-2': features[2],
                'pos_detail-3': features[3],
                'conjugation-form': features[4],
                'conjugation': features[5],
                'standard_form': features[6] if '*' == features[6] else node.surface,
                'reading': features[7] if len(features) > 7 else '',
                'pronunciation': features[8] if len(features) > 8 else ''
            })
            tokens.append(token_feature)
            node = node.next
        return tokens[1:-1] # token of index 0 and -1 is '*'