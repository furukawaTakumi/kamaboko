
import os
import kamaboko


def list():
    resource_dir = f"{os.path.dirname(kamaboko.__file__)}/resource"

    for root, _, files in os.walk(resource_dir):
        level = root.replace(resource_dir, '').count(os.sep)
        dir_indent = ' ' * 4 * level
        print(f"{dir_indent}{os.path.basename(root)}")
        subindent = ' ' * 4 * (level + 1)
        for filename in sorted(files):
            print(f"{subindent}{filename}")