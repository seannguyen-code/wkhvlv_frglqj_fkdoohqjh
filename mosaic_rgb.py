import numpy as np
import argparse
import cv2 as cv
import sys
import os
import PIL
from PIL import Image


def mosaic_rgb(image_path):
    # Read and covert img to np array
    img = Image.open(image_path)
    img_np = np.asarray(img)

    # Data structure
    images = {}
    rgb = ['red', 'green', 'blue']

    # Extrat RGB
    for each in range(3):
        channel = img_np[:, :, each]
        placeholder = np.zeros(img_np.shape, dtype=np.uint8)
        placeholder[:, :, each] = channel
        images[rgb[each]] = placeholder

    # Flip
    images['red'] = cv.flip(images['red'], 1)
    images['green'] = cv.flip(images['green'], -1)
    images['blue'] = cv.flip(images['blue'], 0)

    # Concat
    up = cv.hconcat([img_np, images['blue']])
    down = cv.hconcat([images['red'], images['green']])
    final = cv.vconcat([up, down])
    final = cv.cvtColor(final, cv.COLOR_BGR2RGB)

    return final


n = len(sys.argv)
if n == 2:
    if not os.path.exists('output'):
        os.makedirs('output')

    save_img = mosaic_rgb(sys.argv[1])
    output_path = os.path.join('output', 'mosaic_rgb_' + os.path.basename(sys.argv[1]))
    cv.imwrite(output_path, save_img)
else:
    print('Please provide a picture!!!')
