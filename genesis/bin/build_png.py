#! /usr/bin/env python2

import os
import re
import sys

outdir = './build'

import svg_dom

if __name__ == '__main__':
    fpath = os.path.abspath(sys.argv[1])
    fbasename = os.path.basename(sys.argv[1])

    PIXEL_WIDTH = int(sys.argv[2]) if len(sys.argv) > 2 else 825
    PIXEL_HEIGHT = int(sys.argv[3]) if len(sys.argv) > 3 else 1125

    dom = svg_dom.DOM(fpath)

    for l in dom.layers:
        dom.layer_show(l)

    #excluded = [l for l in dom.layers if l not in included]
    #for l in excluded:
        #dom.layer_hide(l)

    png_fpath = '{}/{}'.format(outdir, fbasename.replace('.svg', '.png'))
    svg_dom.export_png(fpath, png_fpath, PIXEL_WIDTH, PIXEL_HEIGHT)
