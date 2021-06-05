
import argparse, os, csv
from typing import Iterator


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
    action='store_const',
    const='csv',
    type=str
)

args = parser.parse_args()

def install():
    __check_args()
    with open(args.dic_path, 'r') as f:
        data = csv.reader(f, delimiter=__delimiter(args.file_format))

    if args.dic_type == 'noun':
        __construct_noun(data)
    elif args.dic_type == 'collocation':
        __construct_collocation(data)


def __check_args():
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

def __construct_noun(data: Iterator) -> dict:
    dictionary = {}
    for row in data:
        dictionary[row[0]] = row[1]
    return dictionary

def __construct_collocation(data: Iterator) -> dict:
    dictionary = {}
    # for row in data:

def if_not_exists_when_init():
    # 辞書のキーが存在しないとき、dictで初期化
    pass