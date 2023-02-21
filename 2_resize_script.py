
import os
import math
import shutil
import cv2 as cv
import common as c
import pandas as pd
import matplotlib.pyplot as plt

import multiprocessing


def get_type_from_path(path, img_c, batch_no):
    path_n = os.path.dirname(path).split('/')[-1]
    file_name = os.path.basename(path).split('.')[0] + "_" + str(img_c) + "_B_" + str(batch_no) + ".jpg"
    return os.path.join(c.RZD_3_PATH, path_n, file_name)


def resize_img(batch_no, batch_list, mode):
    for i,img in enumerate(batch_list):
        print("Processing Batch: ", batch_no, i, len(batch_list))
        #break;
        mat_img = cv.imread(img, mode)
        try:
            height, width, channel = mat_img.shape
            #print("ORG : ", height, width, channel)
            if width < height:
                factor = c.IMG_SIZE/width
                n_width = c.IMG_SIZE
                n_height = round(height * factor)
                p_img_count = math.ceil(n_height/c.IMG_SIZE)
                rez_img = cv.resize(mat_img, (n_width, n_height), interpolation = cv.INTER_AREA)
                count = 0
                for i in range(p_img_count):
                    if n_height < c.IMG_SIZE:
                        n_height = c.IMG_SIZE
                    end = n_height
                    start = n_height - c.IMG_SIZE
                    n_height -= c.IMG_SIZE
                    n_mat = rez_img[start:end, :, :]
                    cv.imwrite(get_type_from_path(img, count, batch_no), n_mat)
                    count += 1
            else:
                factor = c.IMG_SIZE/height
                n_width = round(width * factor)
                n_height = c.IMG_SIZE
                p_img_count = math.ceil(n_width/c.IMG_SIZE)
                rez_img = cv.resize(mat_img, (n_width, n_height), interpolation = cv.INTER_AREA)
                count = 0
                for i in range(p_img_count):
                    if n_width < c.IMG_SIZE:
                        n_width = c.IMG_SIZE
                    end = n_width
                    start = n_width - c.IMG_SIZE
                    n_width -= c.IMG_SIZE
                    n_mat = rez_img[:, start:end, :]
                    cv.imwrite(get_type_from_path(img, count, batch_no), n_mat)
                    count += 1
        except Exception as e:
            print("Error ", e)
            cv.imwrite(os.path.join(c.DUMP_PATH, img), mat_img)

if __name__ == '__main__':

    if (os.path.exists(c.RZD_3_PATH)) :
        shutil.rmtree(c.RZD_3_PATH)
    print("Creating Structure.")
    
    c.check_or_creat(c.RZD_3_PATH)
    c.check_or_creat(c.RZD_3_HEALTHY)
    c.check_or_creat(c.RZD_3_LEAF_RUST)
    c.check_or_creat(c.RZD_3_STEM_RUST)
    c.check_or_creat(c.RZD_3_SMUT)
    c.check_or_creat(c.DUMP_PATH)
    
    img_list = c.get_img_list()

    print("Total :", len(img_list))
    
    process_list = []
    p_count = multiprocessing.cpu_count() - 2

    element = math.floor(len(img_list)/p_count)

    for p_c in range(p_count):
        start = p_c * element
        end = (p_c + 1) * element
        if p_c == p_count - 1:
            end += len(img_list) % p_count
        print("D - ", p_c, ":",start, end)
        p = multiprocessing.Process(target=resize_img, args=(p_c, img_list[start:end], cv.IMREAD_COLOR, ))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    print("Completed.");