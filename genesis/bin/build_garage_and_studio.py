#! /usr/bin/env python2

import os
import re
import sys

outdir = './build'

import svg_dom

if __name__ == '__main__':
    tmp_svg_path = '/tmp/garage_and_studio.svg'
    fpath = 'garage_and_studio.svg'
    fbasename = fpath

    PIXEL_WIDTH = 3508
    PIXEL_HEIGHT = 2480

    dom = svg_dom.DOM(fpath)

    for l in dom.layers:
        dom.layer_show(l)

    excluded = [l for l in dom.layers if 'studio' in l]
    for l in excluded:
        dom.layer_hide(l)

    dom.write_file(tmp_svg_path)
    png_fpath = '{}/garage.png'.format(outdir)
    pdf_fpath = '{}/garage.pdf'.format(outdir)
    svg_dom.export_png(tmp_svg_path, png_fpath, PIXEL_WIDTH, PIXEL_HEIGHT)
    svg_dom.export_pdf(tmp_svg_path, pdf_fpath)

    for l in dom.layers:
        dom.layer_show(l)

    excluded = [l for l in dom.layers if 'garage' in l]
    for l in excluded:
        dom.layer_hide(l)

    dom.write_file(tmp_svg_path)
    png_fpath = '{}/studio.png'.format(outdir)
    pdf_fpath = '{}/studio.pdf'.format(outdir)
    svg_dom.export_png(tmp_svg_path, png_fpath, PIXEL_WIDTH, PIXEL_HEIGHT)
    svg_dom.export_pdf(tmp_svg_path, pdf_fpath)

