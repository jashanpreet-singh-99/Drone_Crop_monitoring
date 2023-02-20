import os
import math
import multiprocessing

import cv2 as cv
import common as c
import pandas as pd

def dhash(img, size=8):
    row_hash = 0
    col_hash = 0
    for y in range(size):
        for x in range(size):
            row_bit = img[y,x] < img[y,x + 1] 
            row_hash = row_hash << 1 | row_bit
            
            col_bit = img[y,x] < img[y + 1,x]
            col_hash = col_hash << 1 | col_bit
    return format_hex(row_hash, col_hash, size)

# Reference Dhash
# https://github.com/benhoyt/dhash
# https://benhoyt.com/writings/duplicate-image-detection/
#
def format_hex(row_hash, col_hash, size=8):
    """Format dhash integers as hex string of size*size//2 total hex digits
    (row_hash and col_hash concatenated).
    >>> format_hex(19409, 14959, size=4)
    '4bd13a6f'
    >>> format_hex(1, 2, size=4)
    '00010002'
    """
    hex_length = size * size // 4
    return '{0:0{2}x}{1:0{2}x}'.format(row_hash, col_hash, hex_length)

def hash_img(batch_no, batch_list):
    hash_list = []
    for i,img_path in enumerate(batch_list):
        mat_img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
        img = cv.resize(mat_img, (9, 9), interpolation = cv.INTER_AREA)
        h_1 = dhash(img)
        hash_list.append(h_1)
        print("Processing :", batch_no, " -- ", i)
    df = pd.DataFrame({"img":batch_list, "hash": hash_list})
    df.to_csv(os.path.join(c.HASH_PATH, 'b_' + str(batch_no) + "_hash.csv"))


if __name__ == '__main__':
    img_list = c.get_img_list()
    print("Total :", len(img_list))

    process_list = []
    p_count = multiprocessing.cpu_count()

    element = math.floor(len(img_list)/p_count)

    for p_c in range(p_count):
        start = p_c * element
        end = (p_c + 1) * element
        if p_c == p_count - 1:
            end += len(img_list) % p_count
        print("D - ", p_c, ":",start, end)
        p = multiprocessing.Process(target=hash_img, args=(p_c, img_list[start:end], ))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    print("Completed.");