

import CaboCha
from attrdict import AttrDict


class CaboChaAnalyzer():
    def __init__(self) -> None:
        self.cabocha = CaboCha.Parser().parse


    def __call__(self, text):
        output = self.cabocha(text)
        tokens, chunks = self.__conv_to_tokens_and_chunks(output.toString(CaboCha.CABOCHA_FORMAT_LATTICE))
        self.__add_chunk_from_info(chunks)
        return tokens, chunks

    def __conv_to_tokens_and_chunks(self, output: str):
        tokens = []
        chunks = []
        chunk_num = 0
        token = AttrDict()
        chunk = []
        for line in output.splitlines():
            if line.startswith('EOS'):
                chunks.append(chunk)
                break

            if line.startswith('*'):
                dep_features = line.split()
                token.chunk_to = int(dep_features[2][:-1])
                if 0 < len(chunk):
                    chunks.append(chunk)
                    chunk = []
                    chunk_num += 1
            else:
                surface, feature_str = line.split('\t')
                features = feature_str.split(',')
                token.surface = surface
                token.pos = features[0]
                token.pos_detail_1 = features[1]
                token.pos_detail_2 = features[2]
                token.pos_detail_3 = features[3]
                token.conjugation_form = features[4]
                token.conjugation = features[5]
                token.standard_form = features[6] if features[6] != '*' else surface
                token.reading = features[7] if len(features) > 7 else ''
                token.pronunciation = features[8] if len(features) > 8 else ''
                token.belong_to = chunk_num
                tokens.append(token)
                chunk.append(token)
                token = AttrDict()
        return tokens, chunks

    def __add_chunk_from_info(self, chunks):
        for idx, c in enumerate(chunks):
            for token in c:
                if 'chunk_to' in token.keys():
                    chunks[token.chunk_to][0].chunk_from = idx