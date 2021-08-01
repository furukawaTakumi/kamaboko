

class Rules:
    __tigainai_surface = ('違い', 'ない')
    __kamosirenai_surface = ('かも', 'しれる', 'ない')
    __aruzyanai_surface = ('ある', 'じゃ', 'ない')

    @classmethod
    def is_tigainai(cls, chunk):
        if len(chunk) < 2:
            return False
        
        for idx in range(len(chunk) - 1):
            if tuple(map(lambda x: x.standard_form, chunk[idx:idx+2])) == cls.__tigainai_surface:
                return True
        return False

    @classmethod
    def is_kamosirenai(cls, chunk):
        if len(chunk) < 3:
            return False
        for idx in range(len(chunk) - 2):
            if tuple(map(lambda x: x.standard_form, chunk[idx:idx+3])) == cls.__kamosirenai_surface:
                return True
        return False

    @classmethod
    def is_aruzyanai(cls, chunk):
        return cls.__check_surfacies(chunk, cls.__aruzyanai_surface)
    
    @classmethod
    def __check_surfacies(cls, chunk, surfacies):
        if len(chunk) < len(surfacies):
            return False
        for idx in range(len(chunk) - (len(surfacies) - 1)):
            if tuple(map(lambda x: x.standard_form, chunk[idx:idx+3])) == surfacies:
                return True
        return False
