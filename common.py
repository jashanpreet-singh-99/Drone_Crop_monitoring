import os
import shutil

IMG_SIZE = 256

DB_PATH  = os.path.join(os.getcwd(), 'wheat-dataset')
EED_PATH  = os.path.join(os.getcwd(), 'raw_dataset')
RZD_PATH  = os.path.join(os.getcwd(), 'rez_dataset')
RZD_3_PATH  = os.path.join(os.getcwd(), 'rez_dataset_3')
DUMP_PATH = os.path.join(os.getcwd(), 'raw_dataset', '_dump')

RD_PATH = os.path.join(os.getcwd(), 'wheat-dataset', '__gwhd_2021', 'images')

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

RZD_3_HEALTHY   = os.path.join( RZD_3_PATH, C_HEALTHY)
RZD_3_LEAF_RUST = os.path.join( RZD_3_PATH, C_LEAF_RUST)
RZD_3_STEM_RUST = os.path.join( RZD_3_PATH, C_STEM_RUST)
RZD_3_SMUT      = os.path.join( RZD_3_PATH, C_SMUT)

IMG_LABEL = { C_HEALTHY: 'HW',
              C_LEAF_RUST: 'LR',
              C_STEM_RUST: 'SR',
              C_SMUT: 'SM'
            }

HASH_PATH = os.path.join(os.getcwd(), 'hash')
HASH_DB   = os.path.join(os.getcwd(), 'hash', 'Master_hash.csv')

def get_abs_path(file_name, dirr):
    return os.path.join(dirr, file_name)

def get_imgs(img_list, dtype):
    img_h =  os.listdir(dtype)
    img_h = [x for x in img_h if x[0] not in ['.', '_']]
    img_list += list(map(get_abs_path, img_h, [dtype] * len(img_h)))
    return img_list

def get_img_list():
    img_list = []
    img_list = get_imgs(img_list, DIR_HEALTHY)
    img_list = get_imgs(img_list, DIR_LEAF_RUST)
    img_list = get_imgs(img_list, DIR_STEM_RUST)
    img_list = get_imgs(img_list, DIR_SMUT)
    return img_list

def get_r_img_list():
    img_list = []
    img_list = get_imgs(img_list, RZD_HEALTHY)
    img_list = get_imgs(img_list, RZD_LEAF_RUST)
    img_list = get_imgs(img_list, RZD_STEM_RUST)
    img_list = get_imgs(img_list, RZD_SMUT)
    return img_list

def get_r3_img_list():
    img_list = []
    img_list = get_imgs(img_list, RZD_3_HEALTHY)
    img_list = get_imgs(img_list, RZD_3_LEAF_RUST)
    img_list = get_imgs(img_list, RZD_3_STEM_RUST)
    img_list = get_imgs(img_list, RZD_3_SMUT)
    return img_list

def check_or_creat(dir):
    if (not os.path.exists(dir)) :
        os.makedirs(dir)

def rm_dir(dir):
    if (not os.path.exists(dir)) :
        shutil.rmtree(dir)