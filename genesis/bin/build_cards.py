#! /usr/bin/env python2

import os
import re
import sys
from collections import defaultdict

from version import VERSION

outdir = '/tmp/genesis'+VERSION
mask_fpath = outdir + '/mask.png'

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

def make_rounded_version(png_fpath, layer):
    rounded_png_fpath = '{0}/card_cut_{1}.png'.format(outdir, layer)
    svg_dom.run(
        (
            'convert "{0}"'
            + ' -matte {1}'
            + ' -compose DstIn'
            + ' -composite'
            + ' -trim'
            + ' "{2}"'
        ).format(png_fpath, mask_fpath, rounded_png_fpath)
    )

def make_rotated_versions(png_fpath, layer):
    rot350_png_fpath = '{0}/card_rot350_{1}.png'.format(outdir, layer)
    rot10_png_fpath = '{0}/card_rot10_{1}.png'.format(outdir, layer)
    svg_dom.run(
        (
            'convert "{0}"'
            + ' -background none'
            + ' -rotate -10'
            + ' "{1}"'
        ).format(png_fpath, rot350_png_fpath)
    )
    svg_dom.run(
        (
            'convert "{0}"'
            + ' -background none'
            + ' -rotate 10'
            + ' "{1}"'
        ).format(png_fpath, rot10_png_fpath)
    )

def make_card_back(dom, layer):
    d.layer_show(layer)
    others = [l for l in d.layers if l != layer]
    for o in others:
        d.layer_hide(o)
    d.layer_show('back_bg')
    svg_fpath = '{0}/card_{1}.svg'.format(outdir, layer)
    d.write_file(svg_fpath)
    png_fpath = '{0}/card_rect_{1}.png'.format(outdir, layer)
    svg_dom.export_png(svg_fpath, png_fpath, 825, 1125)
    make_rounded_version(png_fpath, layer)

def make_card_front(dom, layer):
    included = [
      l for l in d.layers
      if (
        l == layer
        or
        (
          not re.search('[0-9]', l)
          and
          l.startswith(re.sub('[0-9]+', '_', layer))
        )
        or
        l.startswith('front_')
      )
    ]
    for l in included:
        d.layer_show(l)
    excluded = [l for l in d.layers if l not in included]
    for l in excluded:
        d.layer_hide(l)
    svg_fpath = '{0}/card_{1}.svg'.format(outdir, layer)
    d.write_file(svg_fpath)
    png_fpath = '{0}/card_rect_{1}.png'.format(outdir, layer)
    svg_dom.export_png(svg_fpath, png_fpath, 825, 1125)
    make_rounded_version(png_fpath, layer)

if __name__ == '__main__':
    svg_dom.ensure_dirs(mask_fpath)
    make_mask_cmd = (
      'convert -size "825"x"1125"'
      + ' xc:none'
      + ' -draw "roundrectangle 30,30,795,1095,50,50"'
      + ' {0}'
    ).format(mask_fpath)
    svg_dom.run(make_mask_cmd)

    d = svg_dom.DOM(sys.argv[1])
    for layer in sorted(d.layers.keys()):
        print('-'*40)
        print('     ' + layer)
        print('-'*40)
        if layer.startswith('back'):
            make_card_back(d, layer)
        elif re.search('\d', layer):
            make_card_front(d, layer)
