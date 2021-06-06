
import argparse, os, csv, json, datetime, pathlib
from typing import Iterator


import kamaboko

def install():
    args = __parse_args()
    __check_args(args)

    with open(args.dic_path, 'r') as f:
        data = csv.reader(f, delimiter=__delimiter(args.file_format))
        dictionary = __construct_dict(data, args)

    save_dir = f"{os.path.dirname(kamaboko.__file__)}/resource/{args.dic_type}"
    filename = args.dic_path.split('/')[-1] + datetime.datetime.now().strftime('%Y__%m__%d-%H__%M__%S.json')
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
    with open(f"{save_dir}/{filename}", 'w') as f:
        json.dump(dictionary, f)
    
    print(f"'{args.dic_path}' save to '{save_dir}'. complete.")

def __check_args(args):
    if not os.path.exists(args.dic_path):
        raise FileNotFoundError(f"{args.dic_path} is not found.")

def __delimiter(fmt_str: str):
    return {
        'csv': ',',
        'tsv': '\t'
    }[fmt_str]

def __construct_dict(data: Iterator, args) -> dict:
    dictionary = {}
    for row in data:
        keys = row[args.word_idx].split(' ')
        tmp_dict = dictionary
        for idx in range(0, len(keys)):
            tmp_dict[keys[idx]] = {
                'dic_type': args.dic_type,
                'is_end': False
            }
            if idx == len(keys) - 1:
                tmp_dict[keys[idx]]['is_end'] = True
                tmp_dict[keys[idx]]['polality'] = __polality_label(row[args.polality_idx], args)
            tmp_dict = tmp_dict[keys[idx]]
    return dictionary

def __polality_label(label, args):
    if label in args.positive_labels:
        return 'p'
    elif label in args.negative_labels:
        return 'n'
    else:
        print(f"Convert Warning: neither polality label '{label}' is not contained '{args.positive_labels}' or '{args.negative_labels}'.")
        return 'e'

def __parse_args():
    parser = argparse.ArgumentParser('argument parser')

    parser.add_argument(
        'dic_path',
        help='path of polarity dictionary', 
        metavar='path/to/dictionary',
        type=str
    )
    parser.add_argument(
        'dic_type',
        help='type of dictionary',
        choices=['noun', 'collocation']
    )
    parser.add_argument(
        '--file_format',
        '-ff',
        help='file type',
        default='csv',
        choices=['csv', 'tsv'],
    )
    parser.add_argument(
        '--word_idx',
        '-wi',
        help='index of word column',
        default=0,
        type=int
    )
    parser.add_argument(
        '--polality_idx',
        '-pi',
        help='index of polality column',
        default=1,
        type=int
    )
    parser.add_argument(
        '--positive_labels',
        '-pl',
        action='append',
        help='positive labels',
        default=['p'],
    )
    parser.add_argument(
        '--negative_labels',
        '-nl',
        action='append',
        help='negative labels',
        default=['n'],
    )

    return parser.parse_args()