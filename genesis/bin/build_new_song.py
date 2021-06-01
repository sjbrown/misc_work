#! /usr/bin/env python2

import os
import re
import sys

outdir = './build'

import svg_dom

if __name__ == '__main__':
    fpath = os.path.abspath(sys.argv[1])
    fbasename = os.path.basename(sys.argv[1])

    PIXEL_WIDTH = 2406
    PIXEL_HEIGHT = 1156

    dom = svg_dom.DOM(fpath)

    for l in dom.layers:
        dom.layer_show(l)

    excluded = [l for l in dom.layers if 'bandpractice' in l]
    for l in excluded:
        dom.layer_hide(l)

    tmp_svg_path = '/tmp/genesis_song.svg'
    dom.write_file(tmp_svg_path)

    png_fpath = '{}/{}'.format(outdir, fbasename.replace('.svg', '.png'))
    svg_dom.export_png(tmp_svg_path, png_fpath, PIXEL_WIDTH, PIXEL_HEIGHT)
