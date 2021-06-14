
import os, glob, json


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

    def __load_dict(self, resource_path):
        dictionary = {}
        for dict_type in self.DICT_TYPES:
            file_items = [
                (file_path, os.path.getmtime(file_path))
                for file_path in glob.glob(f"{resource_path}/{dict_type}/*.json")
            ]
            latest_file = sorted(file_items, key=lambda x: x[1], reverse=True)[0][0]
            with open(latest_file, 'rb') as f:
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