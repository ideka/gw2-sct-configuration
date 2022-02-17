#!/usr/bin/python37

from PIL import Image, ImageChops
import math
import os


MARGIN = 5
MIN = 40


def trim(im):
    if im.size[0] < MIN and im.size[1] < MIN:
        return im

    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 1, -100)
    #im.show(diff)
    bbox = pbbox = diff.getbbox()

    #(0, 0, 128, 128)
    #(12, 11, 120, 118)
    if bbox:
        prebox = (0, 0, im.size[0], im.size[1])

        tl = max(bbox[0], bbox[1]) - MARGIN
        br = min(bbox[2], bbox[3]) + MARGIN
        bbox = [tl, tl, br, br]

        #w = bbox[2] - bbox[0]
        #h = bbox[3] - bbox[1]
        #diff = (max(w, h) - min(w, h)) / 2
        #if w > h:
        #    rightway = pbbox[1] - prebox[1] < prebox[3] - pbbox[3]
        #    bbox[1] -= math.floor(diff) if rightway else math.ceil(diff)
        #    bbox[3] += math.ceil(diff) if rightway else math.floor(diff)
        #elif h > w:
        #    rightway = pbbox[0] - prebox[0] < prebox[2] - pbbox[2]
        #    bbox[0] -= math.floor(diff) if rightway else math.ceil(diff)
        #    bbox[2] += math.ceil(diff) if rightway else math.floor(diff)

        return im.crop(bbox)
    return im


def main():
    for img in os.listdir('.'):
        orig = f'original/{img}'

        if not img.endswith('.jpg') or os.path.isfile(orig):
            continue

        print(f'Processing {img}')
        os.rename(img, orig)
        trim(Image.open(orig)).save(img, quality=95, subsampling=0)

if __name__ == '__main__':
    main()
