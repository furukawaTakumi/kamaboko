
import os, argparse


import kamaboko


def delete():
    args = __parse_args()
    file_path = f"{os.path.dirname(kamaboko.__file__)}/resource/{args.dic_type}/{args.dic_name}"
    
    if not os.path.exists(file_path):
        print('file_path', file_path)
        raise FileNotFoundError(f"'{args.dic_name}' does not found.")

    os.remove(file_path)

    print(f"complete delete '{file_path}'.")

def __parse_args():
    parser = argparse.ArgumentParser('argument parser')

    parser.add_argument(
        'dic_type',
        help='type of dictionary',
        metavar='DIC_TYPE',
        choices=['noun', 'collocation']
    )

    parser.add_argument(
        'dic_name',
        help='delete target dictionary.', 
        metavar='DIC_NAME',
        type=str
    )

    return parser.parse_args()
