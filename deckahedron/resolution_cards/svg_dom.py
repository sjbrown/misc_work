#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from lxml import etree
from collections import defaultdict

sys.path.append('/usr/share/inkscape/extensions/')
from simplestyle import parseStyle, parseColor

DEBUG = 0

def export_png(svg, png, width, height):
    cmd_fmt = 'inkscape --export-png=%s --export-width=%s --export-height=%s %s'
    cmd = cmd_fmt % (png, width, height, svg)
    if DEBUG:
        print cmd
    os.system(cmd)

def export_square_png(svg, png):
    return export_png(svg, png, 825, 825)

def export_tall_png(svg, png):
    return export_png(svg, png, 825, 1125)


class DOM(object):
    def __init__(self, svg_file):
        fp = file(svg_file)
        c = fp.read()
        fp.close()
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

    def replace_text(self, title, newtext, ideal_num_chars=None, style=None):
        if style is None:
            style = {}

        for flowroot in self.title_to_elements[title]:
            flowpara = [x for x in flowroot.iterchildren()
                        if 'flowPara' in x.tag][0]
            flowroot.remove(flowpara)
            for i, line in enumerate(newtext.split('\n')):
                paraclone = etree.fromstring(etree.tostring(flowpara))
                paraclone.text = line
                flowroot.append(paraclone)
            num_lines = i

            if ideal_num_chars and len(newtext) < (ideal_num_chars / 1.5):
                style.update({'font-size': '12px'})
            if ideal_num_chars and len(newtext) > (ideal_num_chars - num_lines*20):
                style.update({'font-size': '8px'})

            if style:
                for k,v in style.items():
                    flowroot.attrib['style'] = re.sub(
                      k+':[^;]+;',
                      k+':'+v+';',
                      flowroot.attrib['style']
                    )

    def replace_h1(self, newtext):
        style = {}
        if len(newtext) >= 17:
            words = newtext.split()
            midpoint = len(words)/2
            line1 = ' '.join(words[:midpoint])
            line2 = ' '.join(words[midpoint:])
            newtext = line1 + '\n' + line2
            style = { 'font-size': '16px', 'line-height': '90%' }
        return self.replace_text('h1', newtext, style=style)

    def write_file(self, svg_filename):
        if DEBUG:
            print 'writing file...'
            print svg_filename
        fp = file(svg_filename, 'w')
        fp.write(etree.tostring(self.dom))
        fp.close()



if __name__ == '__main__':
    test()
