#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from lxml import etree
from collections import defaultdict

sys.path.append('/usr/share/inkscape/extensions/')
from simplestyle import parseStyle, parseColor
from version import VERSION

DEBUG = 1

def run(cmd):
    if DEBUG:
        print cmd
    os.system(cmd)

def ensure_dirs(filepath):
    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

def export_png(svg, png, width, height):
    ensure_dirs(png)

    cmd = 'sed -e "s/VERSION/%s/" %s > /tmp/content.svg' % (VERSION, svg)
    run(cmd)

    cmd_fmt = 'inkscape --export-png=%s --export-width=%s --export-height=%s %s'
    cmd = cmd_fmt % (png, width, height, '/tmp/content.svg')
    run(cmd)

def export_pdf(svg, pdf):
    ensure_dirs(pdf)

    cmd_fmt = 'inkscape --export-pdf=%s %s'
    cmd = cmd_fmt % (pdf, svg)
    run(cmd)



class DOM(object):
    def __init__(self, svg_file):
        fp = file(svg_file)
        c = fp.read()
        fp.close()
        c = c.replace('VERSION', VERSION)
        self.dom = etree.fromstring(c)
        self.titles = [x for x in self.dom.getiterator()
                       if x.tag == '{http://www.w3.org/2000/svg}title']
        self.title_to_elements = defaultdict(list)
        for t in self.titles:
            self.title_to_elements[t.text].append(t.getparent())
        self.layers = {
            x.attrib['{http://www.inkscape.org/namespaces/inkscape}label'] : x
            for x in self.dom.getchildren()
            if x.attrib.get('{http://www.inkscape.org/namespaces/inkscape}groupmode') == 'layer'
        }

    def layer_hide(self, layer_label):
        if DEBUG:
            print 'HIDING LAYER', layer_label
        self.layers[layer_label].attrib['style'] = 'display:none'

    def layer_show(self, layer_label):
        self.layers[layer_label].attrib['style'] = 'display:inline'

    def cut_element(self, title):
        for e in self.title_to_elements[title]:
            e.getparent().remove(e)

    def cut_layer(self, layer_label):
        e = self.layers[layer_label]
        if e.getparent():
            e.getparent().remove(e)

    def write_file(self, svg_filename):
        if DEBUG:
            print 'writing file...'
            print svg_filename
        fp = file(svg_filename, 'w')
        fp.write(etree.tostring(self.dom))
        fp.close()



if __name__ == '__main__':
    d = DOM(sys.argv[1])
    i = 0
    for layer in d.layers:
        i += 1
        d.layer_show(layer)
        others = [l for l in d.layers if l != layer]
        for o in others:
            d.layer_hide(o)
        svg_fpath = '/tmp/genesis%s.svg' % i
        pdf_fpath = '/tmp/genesis%s.pdf' % i
        d.write_file(svg_fpath)
        export_pdf(svg_fpath, pdf_fpath)
