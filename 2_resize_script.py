
import os
import math
import shutil
import cv2 as cv
import pandas as pd
import matplotlib.pyplot as plt

import multiprocessing

IMG_SIZE = 256

EED_PATH  = os.path.join(os.getcwd(), 'raw_dataset')
RZD_PATH  = os.path.join(os.getcwd(), 'rez_dataset')
DUMP_PATH = os.path.join(os.getcwd(), 'raw_dataset', '_dump')

C_HEALTHY   = "healthy"
C_LEAF_RUST = "leaf_rust"
C_STEM_RUST = "stem_rust"
C_SMUT     = "smut"

DIR_HEALTHY   = os.path.join( EED_PATH, C_HEALTHY)
DIR_LEAF_RUST = os.path.join( EED_PATH, C_LEAF_RUST)
DIR_STEM_RUST = os.path.join( EED_PATH, C_STEM_RUST)
DIR_SMUT      = os.path.join( EED_PATH, C_SMUT)

RZD_HEALTHY   = os.path.join( RZD_PATH, C_HEALTHY)
RZD_LEAF_RUST = os.path.join( RZD_PATH, C_LEAF_RUST)
RZD_STEM_RUST = os.path.join( RZD_PATH, C_STEM_RUST)
RZD_SMUT      = os.path.join( RZD_PATH, C_SMUT)

IMG_LABEL = { C_HEALTHY: 'HW',
              C_LEAF_RUST: 'LR',
              C_STEM_RUST: 'SR',
              C_SMUT: 'SM'
            }


def check_or_creat(dir):
    if (not os.path.exists(dir)) :
        os.makedirs(dir)


def get_abs_path(file_name, dirr):
    return os.path.join(dirr, file_name)

def get_imgs(img_list, dtype):
    img_h =  os.listdir(dtype)
    img_h = [x for x in img_h if x[0] not in ['.', '_']]
    img_list += list(map(get_abs_path, img_h, [dtype] * len(img_h)))
    return img_list



def get_type_from_path(path, img_c, batch_no):
    path_n = os.path.dirname(path).split('/')[-1]
    file_name = os.path.basename(path).split('.')[0] + "_" + str(img_c) + "_B_" + str(batch_no) + ".jpg"
    return os.path.join( RZD_PATH, path_n, file_name)


def resize_img(batch_no, batch_list):
    for i,img in enumerate(batch_list):
        print("Processing Batch: ", batch_no, i, len(batch_list))
        #break;
        mat_img = cv.imread(img, cv.IMREAD_GRAYSCALE)
        try:
            height, width = mat_img.shape[:2]
            #print("ORG : ", height, width)
            if width < height:
                factor = IMG_SIZE/width
                n_width = IMG_SIZE
                n_height = round(height * factor)
                p_img_count = math.ceil(n_height/IMG_SIZE)
                rez_img = cv.resize(mat_img, (n_width, n_height), interpolation = cv.INTER_AREA)
                count = 0
                for i in range(p_img_count):
                    if n_height < IMG_SIZE:
                        n_height = IMG_SIZE
                    end = n_height
                    start = n_height - IMG_SIZE
                    n_height -= IMG_SIZE
                    n_mat = rez_img[start:end, :]
                    cv.imwrite(get_type_from_path(img, count, batch_no), n_mat)
                    count += 1
            else:
                factor = IMG_SIZE/height
                n_width = round(width * factor)
                n_height = IMG_SIZE
                p_img_count = math.ceil(n_width/IMG_SIZE)
                rez_img = cv.resize(mat_img, (n_width, n_height), interpolation = cv.INTER_AREA)
                count = 0
                for i in range(p_img_count):
                    if n_width < IMG_SIZE:
                        n_width = IMG_SIZE
                    end = n_width
                    start = n_width - IMG_SIZE
                    n_width -= IMG_SIZE
                    n_mat = rez_img[:, start:end]
                    cv.imwrite(get_type_from_path(img, count, batch_no), n_mat)
                    count += 1
        except Exception as e:
            print("Error ", e)
            cv.imwrite(os.path.join(DUMP_PATH, img), mat_img)

if __name__ == '__main__':
    

    shutil.rmtree(RZD_PATH)
    print("Creating Structure.")
    
    check_or_creat(RZD_HEALTHY)
    check_or_creat(RZD_LEAF_RUST)
    check_or_creat(RZD_STEM_RUST)
    check_or_creat(RZD_SMUT)
    check_or_creat(DUMP_PATH)
    
    img_list = []
    img_list = get_imgs(img_list, DIR_HEALTHY)
    img_list = get_imgs(img_list, DIR_LEAF_RUST)
    img_list = get_imgs(img_list, DIR_STEM_RUST)
    img_list = get_imgs(img_list, DIR_SMUT)

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
        p = multiprocessing.Process(target=resize_img, args=(p_c, img_list[start:end], ))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    print("Completed.");