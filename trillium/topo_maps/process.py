#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
from lxml import etree
from itertools import product


def export_png(svg, png):
    cmd_fmt = 'inkscape --export-png=%s --export-width=825 --export-height=825 %s'
    cmd = cmd_fmt % (png, svg)
    print cmd
    os.system(cmd)

class DOM(object):
    def __init__(self, svg_file):
        fp = file(svg_file)
        c = fp.read()
        fp.close()
        self.dom = etree.fromstring(c)
        self.titles = [x for x in self.dom.getiterator()
                       if x.tag == '{http://www.w3.org/2000/svg}title']
        self.title_to_element = {
            t.text: t.getparent()
            for t in self.titles
        }

    def id_of(self, title):
        e = self.title_to_element[title]
        return e.attrib['id']

    def cut_element(self, title):
        e = self.title_to_element[title]
        e.getparent().remove(e)

    def write_file(self, svg_filename):
        print svg_filename
        fp = file(svg_filename, 'w')
        fp.write(etree.tostring(self.dom))
        fp.close()

lines = ['l%02d' % x for x in range(1,36)]

def filter_dom_elements(dom, title):
    for other_line in [x for x in lines if x != title]:
        dom.cut_element(other_line)
    dom.cut_element('post_hole_1')
    dom.cut_element('post_hole_2')
    dom.cut_element('outline_box')


def make_topo():
    for i, title in enumerate(lines):
        dom = DOM('topo_inprogress.svg')

        filter_dom_elements(dom, title)
        svg_filename = '/tmp/topo/topo_%s.svg' % title

        dom.write_file(svg_filename)

        cmd = 'inkscape --select=%s --select=%s --verb=SelectionDiff --verb=FileSave --verb=FileQuit %s' % (dom.id_of('box'), dom.id_of(title), svg_filename)
        print cmd
        os.system(cmd)



if not os.path.exists('/tmp/topo'):
    os.makedirs('/tmp/topo')
make_topo()
