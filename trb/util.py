import os
import re
from os.path import exists

def lower_key(dictionary):
    """
    Non-recursive replacement of keys with lowercase values for consistency
    :param dictionary:
    :return:
    """
    new_dict = {}
    for key in dictionary.keys():
        new_dict[key.lower()] = dictionary[key]

    return new_dict


def strip_field_name(line: str):
    return line.split(":", 1)[-1].strip()


def files_present(path, file_type):
    if exists(path):

        dir = os.listdir(path)
        for file in dir:
            if file.endswith(file_type):
                return True

    return False

def filtered_ls(dir_path, endings):
    files = os.listdir(dir_path)
    returns = []
    for file in files:
        if file.endswith(endings):
            returns.append(file)

    return returns

def get_title_number(filename):
    res = re.search(r"(?<=_t)[0-9]{2}(?=\.mkv)", filename)
    if res:
        return int(res.group(0))
    else:
        return -1