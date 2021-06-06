
import argparse, os, csv, json, datetime, pathlib
from typing import Iterator


import kamaboko

def install():
    args = __parse_args()
    __check_args(args)

    with open(args.dic_path, 'r') as f:
        data = csv.reader(f, delimiter=__delimiter(args.file_format))
        dictionary = __construct_dict(data)

    save_dir = f"{os.path.dirname(kamaboko.__file__)}/resource/{args.dic_type}"
    filename = args.dic_path.split('/')[-1] + datetime.datetime.now().strftime('%Y__%m__%d-%H__%M__%S.json')
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
    with open(f"{save_dir}/{filename}", 'w') as f:
        json.dump(dictionary, f)
    
    print(f"'{args.dic_path}' save to '{save_dir}'. complete.")

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
        metavar='noun/collocation',
        type=str
    )
    parser.add_argument(
        '--file_format',
        help='file type',
        metavar='csv/tsv',
        default='csv',
        choices=['csv', 'tsv'],
    )

    return parser.parse_args()

def __check_args(args):
    if not os.path.exists(args.dic_path):
        raise FileNotFoundError(f"{args.dic_path} is not found.")

    if not args.dic_type in ['noun', 'collocation']:
        raise KeyError(f"{args.dic_type} is unkown type of dictionary.")
    
    if not args.file_format in ['csv', 'tsv']:
        raise KeyError(f"{args.file_format} is not supported.")

def __delimiter(fmt_str: str):
    return {
        'csv': ',',
        'tsv': '\t'
    }[fmt_str]

def __construct_dict(data: Iterator) -> dict:
    dictionary = {}
    for row in data:
        dictionary[row[0]] = row[1]
    return dictionary