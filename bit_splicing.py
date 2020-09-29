import numpy as np
import argparse
import cv2 as cv
import sys
import os
import PIL
from PIL import Image


def bit_splicing(image_path):
    # Read the image in greyscale
    img = cv.imread(image_path)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_h, img_w = img_gray.shape

    # Iterate over each pixel and change pixel value to String of binary and then store them.
    img_binaryForm = []
    for i in range(img_h):
        for j in range(img_w):
            img_binaryForm.append((np.binary_repr(img_gray[i][j], width=8)))

    # Data structure
    images = {}
    bit_planes = [str(i+1) + '_bit_plane' for i in range(8)]

    # Extract each plane
    for idx, plane in enumerate(bit_planes):
        #print("i[{}], idx:{}, plane: {}, 2(n-1): {}".format(8-idx-1, idx, plane, 2**idx))
        images[plane] = (np.array([int(i[(8-idx-1)]) for i in img_binaryForm],
                                  dtype=np.uint8)*(2**idx)).reshape(img_h, img_w)

    # Concat
    up = cv.hconcat([images[bit_planes[0]], images[bit_planes[1]],
                     images[bit_planes[2]], images[bit_planes[3]]])
    down = cv.hconcat([images[bit_planes[4]], images[bit_planes[5]],
                       images[bit_planes[6]], images[bit_planes[7]]])
    final = cv.vconcat([up, down])

    return final


n = len(sys.argv)
if n == 2:
    if not os.path.exists('output'):
        os.makedirs('output')

    save_img = bit_splicing(sys.argv[1])
    cv.imwrite('output\\bit_splicing' + sys.argv[1], save_img)
else:
    print('Please provide a picture!!!')
