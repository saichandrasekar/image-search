# read all image names in database directory
import glob

import numpy as np
import scipy

import cv2


def hash_array_to_hash_hex(hash_array):
    # convert hash array of 0 or 1 to hash string in hex
    hash_array = np.array(hash_array, dtype=np.uint8)
    hash_str = ''.join(str(i) for i in 1 * hash_array.flatten())
    return hex(int(hash_str, 2))


def hash_hex_to_hash_array(hash_hex):
    # convert hash string in hex to hash values of 0 or 1
    hash_str = int(hash_hex, 16)
    array_str = bin(hash_str)[2:]
    return np.array([i for i in array_str], dtype=np.float32)

def get_dct_val(name):
    img = cv2.imread(name)
    # resize image and convert to gray scale
    img = cv2.resize(img, (64, 64))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.array(img, dtype=np.float32)
    # calculate dct of image
    dct = cv2.dct(img)
    # to reduce hash length take only 8*8 top-left block
    # as this block has more information than the rest
    dct_block = dct[: 8, : 8]
    # caclulate mean of dct block excluding first term i.e, dct(0, 0)
    dct_average = (dct_block.mean() * dct_block.size - dct_block[0, 0]) / (dct_block.size - 1)
    # convert dct block to binary values based on dct_average
    dct_block[dct_block < dct_average] = 0.0
    dct_block[dct_block != 0] = 1.0

    return hash_array_to_hash_hex(dct_block.flatten())

#W:\06-chan\01-workspace\test-data\archive\dataset\frost
image_names = sorted(glob.glob('./../test-data/archive/dataset/frost/*.jpg'))

# hash dictionary to store hash values on images
image_hash_dict = {}

# for every image calculate PHash value
#print(image_names)
print("Image Repository Scanning in progress..")
for name in image_names:
    img = cv2.imread(name)
    # resize image and convert to gray scale
    img = cv2.resize(img, (64, 64))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.array(img, dtype=np.float32)
    # calculate dct of image
    dct = cv2.dct(img)
    # to reduce hash length take only 8*8 top-left block
    # as this block has more information than the rest
    dct_block = dct[: 8, : 8]
    # caclulate mean of dct block excluding first term i.e, dct(0, 0)
    dct_average = (dct_block.mean() * dct_block.size - dct_block[0, 0]) / (dct_block.size - 1)
    # convert dct block to binary values based on dct_average
    dct_block[dct_block < dct_average] = 0.0
    dct_block[dct_block != 0] = 1.0
    # store hash value

    #print("Image Name: ",name)
    image_hash_dict[name] = hash_array_to_hash_hex(dct_block.flatten())
print("Image Repository Scanning complete...")


print("Image Searching in progress...")
# testing
test_image_location = "./test-data/qwe123.jpg"

hex_val = get_dct_val(test_image_location)

found = False;

matching_image_location = ""
for image_name in image_hash_dict.keys():
    matching_image_location = image_name
    distance = scipy.spatial.distance.hamming(
        hash_hex_to_hash_array(image_hash_dict[image_name]),
        hash_hex_to_hash_array(hex_val)
    )
    #print("{0:<30} {1}".format(image_name, distance))

    if(distance==0.0):
        found = True
        break

if(found):
    print("Image matching...:",matching_image_location)
else:
    print("Image is not matching...")





