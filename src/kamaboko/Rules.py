

class Rules:
    __tigainai_surface = ('違い', 'ない')
    __kamosirenai_surface = ('かも', 'しれる', 'ない')
    __aruzyanai_surface = ('ある', 'じゃ', 'ない')

    @classmethod
    def is_tigainai(cls, chunk):
        return cls.__check_surfacies(chunk, cls.__tigainai_surface)

    @classmethod
    def is_kamosirenai(cls, chunk):
        return cls.__check_surfacies(chunk, cls.__kamosirenai_surface)

    @classmethod
    def is_aruzyanai(cls, chunk):
        return cls.__check_surfacies(chunk, cls.__aruzyanai_surface)
    
    @classmethod
    def __check_surfacies(cls, chunk, surfacies):
        if len(chunk) < len(surfacies):
            return False
        for idx in range(len(chunk) - (len(surfacies) - 1)):
            if tuple(map(lambda x: x.standard_form, chunk[idx:idx+len(surfacies)])) == surfacies:
                return True
        return False
