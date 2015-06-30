#!/usr/bin/env python

import argparse
import os

from PIL import Image, ImageDraw

RED = (228, 3, 3)
ORANGE = (255, 140, 0)
YELLOW = (255, 237, 0)
GREEN = (0, 128, 38)
BLUE = (0, 77, 255)
VIOLET = (117, 7, 135)
TRANS = (255, 255, 255, 0)

RAINBOW = (RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET)


def stripes_info(size, opacity, direction=None):
    color_amount = len(RAINBOW)

    if direction is not None:
        dtn = {'h': 1, 'v': -1}.get(direction)
    else:
        dtn = 1 if size[0] <= size[1] else -1

    if dtn == -1:
        short_side = min(size)
        long_side = max(size)
    else:
        short_side = size[0]
        long_side = size[1]
    step = long_side // color_amount

    return map(lambda color, xy1, xy2: ([(0, xy1)[::dtn], (short_side, xy2)[::dtn]], color),
               [color + (opacity, ) for color in RAINBOW],
               [i*step for i in range(0, color_amount)],
               [i*step for i in range(1, color_amount)] + [long_side]
               )


def draw_rainbow(size, opacity, direction=None):
    flag = Image.new('RGBA', size, TRANS)
    step = size[1] // len(RAINBOW)

    draw = ImageDraw.Draw(flag)

    for i in stripes_info(size, opacity, direction):
        draw.rectangle(*i)

    return flag


def rainbowify(image, opacity, direction=None):
    base = image.convert('RGBA')
    flag = draw_rainbow(base.size, opacity, direction)
    output = Image.alpha_composite(base, flag)
    return output


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('image',
                           help='path to the image file')
    argparser.add_argument('-o', '--out',
                           type=str,
                           help='output filename')
    argparser.add_argument('-f', '--format',
                           type=str,
                           choices=['jpeg', 'png'],
                           help='output image format')
    argparser.add_argument('-p', '--opacity',
                           type=int,
                           default=110,
                           help='opacity of the rainbow flag')
    argparser.add_argument('-d', '--direction',
                           type=str,
                           choices=['v', 'h'],
                           help='direction of rainbow stripes: [v]ertical, [h]orizontal')

    args = argparser.parse_args()

    with Image.open(args.image) as image:
        fmt = args.format or image.format
        output = rainbowify(image, args.opacity, args.direction)
        oldname = os.path.basename(args.image)
        filename = args.out or 'lovewins_' + oldname.split('.')[0] + '.' + fmt.lower()
        output.save(filename, format=fmt)


if __name__ == '__main__':
    main()

