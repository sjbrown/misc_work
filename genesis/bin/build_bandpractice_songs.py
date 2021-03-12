#! /usr/bin/env python2

import os
import re
import sys
from collections import defaultdict

from version import VERSION

outdir = '/tmp/genesis'+VERSION

import svg_dom
#  def run(cmd):
#  def ensure_dirs(filepath):
#  def export_png(svg, png, width, height):
#  def export_pdf(svg, pdf):
#  class DOM(object):
#    def __init__(self, svg_file):
#    def layer_hide(self, layer_label):
#    def layer_show(self, layer_label):
#    def cut_element(self, title):
#    def cut_layer(self, layer_label):
#    def write_file(self, svg_filename):

def make_front(dom, layer):
    included = [
      l for l in d.layers
      if (
        l == layer
        or
        'bg' in l
      )
    ]
    for l in included:
        d.layer_show(l)
    excluded = [l for l in d.layers if l not in included]
    for l in excluded:
        d.layer_hide(l)
    svg_fpath = '{0}/{1}.svg'.format(outdir, layer)
    d.write_file(svg_fpath)
    png_fpath = '{0}/{1}.png'.format(outdir, layer)
    svg_dom.export_png(svg_fpath, png_fpath, 2406, 1156)

if __name__ == '__main__':
    svg_dom.ensure_dirs(outdir + '/foo.txt')
    d = svg_dom.DOM(sys.argv[1])
    for layer in sorted(d.layers.keys()):
        print('-'*40)
        print('     ' + layer)
        print('-'*40)
        if re.search('\d', layer):
            make_front(d, layer)
