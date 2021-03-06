
import os, glob, json
from pathlib import Path
from collections import defaultdict

import kamaboko


class PolalityDict():
    DICT_TYPES = ['noun', 'collocation'] # start with lowest priority
    
    @property
    def NEGATION_WORDS(self):
        return ['ない', 'ぬ', 'ん']

    def __init__(self):
        self.resource_path = f"{os.path.dirname(kamaboko.__file__)}/resource"
        self.__check_exist_dictionary(self.resource_path)
        self.dictionary = self.__load_dict(self.resource_path)
        self.__define_dict_methods()
    
    def is_negation(self, token):
        if  token.standard_form == 'ん' \
        and token.pos == '名詞' \
        and token.pos_detail_1 == '非自立' \
        and token.pos_detail_2 == '一般':
            return False # 否定でない「あるんじゃない」などを否定としないため

        if token.standard_form in self.NEGATION_WORDS:
            return True
        else:
            return False

    def __load_dict(self, resource_path):
        dictionary = defaultdict(lambda: 0)
        for dict_type in self.DICT_TYPES:
            file_items = [
                (Path(file_path), os.path.getmtime(file_path))
                for file_path in glob.glob(f"{resource_path}/{dict_type}/*")
            ]
            for file_item in sorted(file_items, key=lambda x: x[1]):
                with file_item[0].open('rb') as f:
                    dictionary.update(json.load(f))
        return dictionary

    def __check_exist_dictionary(self, resource_path: str):
        file_cnt = 0
        for dict_type in self.DICT_TYPES:
            file_cnt += len(os.listdir(f"{resource_path}/{dict_type}"))
        
        if 0 == file_cnt:
            raise FileNotFoundError(f"'{dict_type}' type dictionary is not exists.")

    def __define_dict_methods(self):
        # black masic
        import inspect
        from collections.abc import Mapping
        for func_name, _ in inspect.getmembers(Mapping, inspect.isfunction):
            mapping_func = eval(f"Mapping.{func_name}")
            func_args = mapping_func.__code__.co_varnames[:mapping_func.__code__.co_argcount]
            if hasattr(self.dictionary, func_name):
                indent = ' ' * 4
                exec(f"def {func_name}({', '.join(func_args)}):\n{indent}return self.dictionary.{func_name}({', '.join(func_args[1:])})")
                exec(f"PolalityDict.{func_name} = {func_name}")