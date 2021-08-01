from copy import deepcopy


class DisplayFilter:
    def __init__(self, display_keys = set()) -> None:
        analyzer_added_key = {
            'surface',
            'pos',
            'pos_detail_1',
            'pos_detail_2',
            'pos_detail_3',
            'conjugation_form',
            'conjugation',
            'standard_form',
            'reading',
            'pronunciation',
            'belong_to',
            'chunk_to',
        }
        kamaboko_added_key = {
            'polality',
            'is_parallel_start',
            'is_collocation_parts',
            'is_parallel_end',
            'negation_count',
            'is_subject',
            'is_scaned',
            'is_aruzyanai',
            'is_tigainai',
            'is_kamosirenai'
        }
        default_keys = kamaboko_added_key | analyzer_added_key
        if len(display_keys) == 0:
            self.display_keys = default_keys
        else:
            self.display_keys = default_keys & display_keys
            not_found_key = (display_keys ^ default_keys) - default_keys
            if 0 < len(not_found_key):
                for key in not_found_key:
                    print(f"Warning: not found '{key}' in all keys")

    def done(self, tokens):
        token_items = deepcopy(tokens)

        for t in token_items:
            delete_items = set(t.keys()) - self.display_keys
            order = 'del ' + ', '.join(["t['%s']" % i for i in delete_items])

            if 4 < len(order):
                exec(order)
        return [
            {k: i[k] for k in i} for i in token_items
        ]
        