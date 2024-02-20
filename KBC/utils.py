import re
import numpy as np
import os

def extract_last_number(s):
    numbers = re.findall(r'[0-9]*\.?[0-9]+', s)
    if numbers:
        last_number = numbers[-1]
        if '.' in last_number:
            return float(last_number)
        else:
            return int(last_number)
    return None

def find_indexes(arr, value):
    if type(arr) == np.ndarray:
        return np.where(arr == value)[0].tolist()
    return find_indexes(np.array(arr), value)

def index_to_id(indexes):
    if type(indexes) == np.ndarray:
        return (indexes + 1).tolist()
    return index_to_id(np.array(indexes))

def makedirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 3, 3]
    print(find_indexes(arr, 3))