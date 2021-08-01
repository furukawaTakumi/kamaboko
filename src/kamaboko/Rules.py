

class Rules:
    __tigainai_surface = ('違い', 'ない')

    @classmethod
    def is_tigainai(cls, chunk):
        if len(chunk) < 2:
            return False
        
        for idx in range(len(chunk) - 1):
            if tuple(map(lambda x: x.standard_form, chunk[idx:idx+2])) == cls.__tigainai_surface:
                return True
        return False