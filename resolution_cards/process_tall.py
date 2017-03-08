#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
from lxml import etree
from itertools import product
from tall_cards import cards

def export_png(svg, png):
    cmd_fmt = 'inkscape --export-png=%s --export-width=825 --export-height=1125 %s'
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

    def cut_element(self, title):
        e = self.title_to_element[title]
        e.getparent().remove(e)

    def replace_text(self, title, newtext, max_chars=None):
        flowroot = self.title_to_element[title]
        flowpara = [x for x in flowroot.iterchildren() if 'flowPara' in x.tag][0]
        flowroot.remove(flowpara)
        for i, line in enumerate(newtext.split('\n')):
            paraclone = etree.fromstring(etree.tostring(flowpara))
            paraclone.text = line
            flowroot.append(paraclone)
        num_lines = i

        if max_chars and len(newtext) > (max_chars - num_lines*20):
            flowroot.attrib['style'] = re.sub(
                'font-size:\d+px;', 'font-size:8px;', flowroot.attrib['style']
            )

    def write_file(self, svg_filename):
        print svg_filename
        fp = file(svg_filename, 'w')
        fp.write(etree.tostring(self.dom))
        fp.close()


def filter_dom_elements(dom, card):
    cut_these = [
      'mod_str', 'mod_int', 'mod_dex', 'mod_bond',
      'wiz_ne', 'wiz_e', 'wiz_se', 'wiz_sw', 'wiz_w', 'wiz_nw',
      'rogue_ne', 'rogue_e', 'rogue_se', 'rogue_sw', 'rogue_w', 'rogue_nw',
      'fighter_ne', 'fighter_e', 'fighter_se', 'fighter_sw', 'fighter_w', 'fighter_nw',
    ]
    if card.get('class_pos'):
        [cut_these.remove(x) for x in card['class_pos']]
    if card.get('mod'):
        keep = 'mod_' + card['mod'].lower()
        cut_these.remove(keep)
    for x in cut_these:
        dom.cut_element(x)


# Example Card:
{'desc_10': 'Success',
 'desc_79': 'Stumble, hesitate\nor flinch',
 'desc_detail': 'When you act despite an imminent threat, say how you deal with it and roll. If you do it... * by powering through or enduring, roll +Str * by getting out of the way or acting fast, roll +Dex * with quick thinking or through mental fortitude, roll +Int On a 7-9, you stumble, hesitate, or flinch: the GM will offer you a worse outcome, hard bargain, or ugly choice',
 'h1': 'Defy Danger',
 'label_10': True,
 'label_79': True,
 'mod_shield': False,
 'mod_str': ''
}

def one_blank_front():
    dom = DOM('tall_card_front.svg')

    print '\nWorking on Blank Front card'
    print '\n'

    filter_dom_elements(dom, {})
    dom.replace_text('desc_79', '', max_chars=40)
    dom.replace_text('desc_10', '', max_chars=40)
    dom.replace_text('desc_detail', '', max_chars=300)
    dom.replace_text('h1', '')

    # Create the svg file and export a PNG
    svg_filename = '/tmp/tall_cards/deck_card_face_blank.svg'
    png_filename = '/tmp/tall_cards/deck_card_face_blank.png'
    dom.write_file(svg_filename)
    export_png(svg_filename, png_filename)


def make_deck():
    export_png('tall_card_back.svg', '/tmp/tall_cards/back.png')

    one_blank_front()

    for i, card in enumerate(cards):
        dom = DOM('tall_card_front.svg')

        print '\nWorking on ' + card['h1']
        print '\n'

        filter_dom_elements(dom, card)
        dom.replace_text('desc_79', card['desc_79'], max_chars=40)
        dom.replace_text('desc_10', card['desc_10'], max_chars=40)
        dom.replace_text('desc_detail', card['desc_detail'], max_chars=300)
        dom.replace_text('h1', card['h1'])

        # Create the svg file and export a PNG
        svg_filename = '/tmp/tall_cards/deck_card_face%02d.svg' % ((i+1))
        png_filename = '/tmp/tall_cards/deck_card_face%02d.png' % ((i+1))

        dom.write_file(svg_filename)

        export_png(svg_filename, png_filename)


if __name__ == '__main__':
    if not os.path.exists('/tmp/tall_cards'):
        os.makedirs('/tmp/tall_cards')
    make_deck()
