from typing import List, Dict
import os


def find_files(ext: str, where: str=None, recursive: bool = False) -> List[str]:
    # Set search directory
    if where is None:
        search_dir = os.getcwd()
    else:
        search_dir = where

    return find_multiple([ext], [search_dir], recursive)


def find_multiple(ext_list: List[str], dir_list: List[str], recursive: bool = False) -> List[str]:

    # Sanitize input
    ext_list = list(map(lambda x: x if x[0] is '.' else "." + x, ext_list))
    dir_list = list(map(lambda x: x if x[len(x) - 1] is '/' else x + "/", dir_list))

    # Compute result
    result: List[str] = []

    # Walk the directory tree
    for search_dir in dir_list:
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                for ext in ext_list:
                    if file.endswith(ext):
                        result.append(os.path.join(root, file))

            if not recursive:
                break

    return result


def default_map(src_files: List[str], where: str = None) -> Dict[str, str]:
    result = {}

    # Handle in-place vs out-of-place build mappings
    if where is None:
        for file in src_files:
            result[file] = os.path.splitext(file)[0] + ".o"

        return result
    else:
        for file in src_files:
            with_ext = str(os.path.basename(file))
            no_ext = os.path.splitext(with_ext)[0]

            if where[len(where) - 1] is '/':
                result[file] = where + no_ext + ".o"
            else:
                result[file] = where + "/" + no_ext + ".o"

        return result
