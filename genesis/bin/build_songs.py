#! /usr/bin/env python2

import os
import re
import sys

from version import VERSION

builddir = '/tmp/genesis'+VERSION
outdir = './build'

import svg_dom

def make_front(dom, layer):
    included = [
      l for l in dom.layers
      if (
        l == layer
        or
        'bg' in l
      )
    ]
    for l in included:
        dom.layer_show(l)
    excluded = [l for l in dom.layers if l not in included]
    for l in excluded:
        dom.layer_hide(l)
    svg_fpath = '{0}/{1}.svg'.format(builddir, layer)
    dom.write_file(svg_fpath)
    png_fpath = '{0}/{1}.png'.format(outdir, layer)
    svg_dom.export_png(svg_fpath, png_fpath, 2406, 1156)

if __name__ == '__main__':
    d = svg_dom.DOM('songs.svg')
    for layer in sorted(d.layers.keys()):
        print('-'*40)
        print('     ' + layer)
        print('-'*40)
        if re.search('\d', layer):
            make_front(d, layer)
