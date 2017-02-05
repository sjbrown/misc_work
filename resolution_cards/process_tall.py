#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
from lxml import etree
from itertools import product
from tall_cards import cards

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

    def cut_element(self, title):
        e = self.title_to_element[title]
        e.getparent().remove(e)

    def replace_text(self, title, newtext):
        flowroot = self.title_to_element[title]
        print 'fr', flowroot
        print 'fps', [x for x in flowroot.iterchildren() if 'flowPara' in x.tag]
        flowpara = [x for x in flowroot.iterchildren() if 'flowPara' in x.tag][0]
        flowpara.text = newtext

    def write_file(self, svg_filename):
        print svg_filename
        fp = file(svg_filename, 'w')
        fp.write(etree.tostring(self.dom))
        fp.close()


def filter_dom_elements(dom, card, deck_title, dice_rule):
        for dt in ['deck_1', 'deck_2', 'deck_3', 'deck_4']:
            if dt == deck_title:
                continue
            dom.cut_element(dt)

        if not card.get('blessing'):
            dom.cut_element('copper_halo')
            dom.cut_element('gold_halo')
        elif card.get('blessing') == 'copper':
            dom.cut_element('gold_halo')
        elif card.get('blessing') == 'gold':
            dom.cut_element('copper_halo')

        if not card.get('crit_win'):
            dom.cut_element('crit_win')

        if not card.get('crit_fail'):
            dom.cut_element('crit_fail')

        if not card.get('Pro'):
            dom.cut_element('proficient')

        if not card.get('Tmark'):
            dom.cut_element('exhaustable')

        # Choose the dice pips to print out
        for titletuple in product(
            ['four', 'six'],
            ['nw', 'ne', 'sw', 'se'],
            ['1', '2']
        ):
            title = '_'.join(titletuple)
            if title not in dice_rule:
                dom.cut_element(title)

        # Choose how many ✔s and ✗s to show
        letter_to_prefix = {
          'a': 'anchor',
          'b': 'bulb',
          'c': 'crescent',
          'd': 'dart',
        }
        score_to_suffix = {
          1: '_two_x',
          2: '_one_x',
          3: '_one_check',
          4: '_two_check',
        }
        suffixes = score_to_suffix.values()
        for letter, prefix in letter_to_prefix.items():
            for suffix in suffixes:
                title = prefix + suffix
                if title != prefix + score_to_suffix[card[letter]]:
                    dom.cut_element(title)


def make_deck():
    export_png('tall_card_back.svg', '/tmp/tall_cards/back.png')

    for i, card in enumerate(cards):
        dom = DOM('tall_card_front.svg')

        dom.replace_text('desc_79', card['desc_79'])

        # Create the svg file and export a PNG
        svg_filename = '/tmp/tall_cards/deck_card_face%02d.svg' % ((i+1))
        png_filename = '/tmp/tall_cards/deck_card_face%02d.png' % ((i+1))

        dom.write_file(svg_filename)

        export_png(svg_filename, png_filename)


if __name__ == '__main__':
    if not os.path.exists('/tmp/tall_cards'):
        os.makedirs('/tmp/tall_cards')
    make_deck()
