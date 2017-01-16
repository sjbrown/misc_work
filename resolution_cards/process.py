#! /usr/bin/env python

import os
from lxml import etree
from itertools import product
from cards import cards, blessing_cards, dice_print_rules


'''
 title_to_element

{'anchor_one_check': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1cb0>,
 'anchor_one_x': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1d40>,
 'anchor_two_check': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1cf8>,
 'anchor_two_x': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1d88>,
 'bulb_one_check': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1a70>,
 'bulb_one_x': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1b00>,
 'bulb_two_check': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1ab8>,
 'bulb_two_x': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1b48>,
 'crescent_one_check': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1b90>,
 'crescent_one_x': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1c20>,
 'crescent_two_check': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1bd8>,
 'crescent_two_x': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1c68>,
 'dart_one_check': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a18c0>,
 'dart_one_x': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a19e0>,
 'dart_two_check': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1998>,
 'dart_two_x': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1a28>,
 'deck_1': <Element {http://www.w3.org/2000/svg}rect at 0x7f63b24a1878>,
 'deck_2': <Element {http://www.w3.org/2000/svg}rect at 0x7f63b24a1830>,
 'deck_3': <Element {http://www.w3.org/2000/svg}rect at 0x7f63b24a1710>,
 'deck_4': <Element {http://www.w3.org/2000/svg}rect at 0x7f63b24a16c8>,
 'exhaustable': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1950>,
 'proficient': <Element {http://www.w3.org/2000/svg}g at 0x7f63b24a1908>}

cards

[{'Pro': False, 'Tmark': False, 'a': 1, 'b': 1, 'c': 1, 'd': 1},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 2, 'c': 4, 'd': 1},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 2, 'c': 3, 'd': 2},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 4, 'c': 3, 'd': 4},
 {'Pro': True, 'Tmark': False, 'a': 2, 'b': 2, 'c': 3, 'd': 4},
 {'Pro': True, 'Tmark': False, 'a': 2, 'b': 3, 'c': 2, 'd': 3},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 1, 'c': 2, 'd': 3},
 {'Pro': False, 'Tmark': False, 'a': 2, 'b': 1, 'c': 2, 'd': 3},
 {'Pro': False, 'Tmark': False, 'a': 2, 'b': 2, 'c': 1, 'd': 2},
 {'Pro': False, 'Tmark': False, 'a': 3, 'b': 1, 'c': 2, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 4, 'b': 4, 'c': 4, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 1, 'b': 3, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 3, 'c': 4, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 1, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 1, 'b': 2, 'c': 2, 'd': 4},
 {'Pro': True, 'Tmark': True, 'a': 3, 'b': 2, 'c': 1, 'd': 4},
 {'Pro': True, 'Tmark': True, 'a': 1, 'b': 4, 'c': 4, 'd': 2},
 {'Pro': True, 'Tmark': True, 'a': 3, 'b': 4, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 4, 'b': 3, 'c': 4, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 3, 'c': 1, 'd': 3}]
'''


def make_deck(deck_number):
    fp = file('face_ready_to_split.svg')
    c = fp.read()
    fp.close()

    cmd_fmt = 'inkscape --export-png=%s --export-width=825 --export-height=825 %s'
    cmd = cmd_fmt % ('/tmp/cards/back.png', 'back_ready_to_print.svg')
    print cmd
    os.system(cmd)

    for i, card in enumerate(cards):
        svg_filename = '/tmp/cards/deck_%s_card_face%s.svg' % (deck_number, (i+1))
        png_filename = '/tmp/cards/deck_%s_card_face%s.png' % (deck_number, (i+1))
        cmd = cmd_fmt % (png_filename, svg_filename)

        dom = etree.fromstring(c)
        titles = [x for x in dom.getiterator()
                  if x.tag == '{http://www.w3.org/2000/svg}title']
        title_to_element = {
            t.text: t.getparent()
            for t in titles
        }
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

        def cut_element(title):
            e = title_to_element[title]
            e.getparent().remove(e)

        deck_title = 'deck_%s' % deck_number
        for dt in ['deck_1', 'deck_2', 'deck_3', 'deck_4']:
            if dt == deck_title:
                continue
            cut_element(dt)

        if not card.get('blessing'):
            cut_element('copper_halo')
            cut_element('gold_halo')

        if not card.get('crit_win'):
            cut_element('crit_win')

        if not card.get('crit_fail'):
            cut_element('crit_fail')

        if not card.get('Pro'):
            cut_element('proficient')

        if not card.get('Tmark'):
            cut_element('exhaustable')

        dice_rule = dice_print_rules[i][1]
        dice_rule = dice_rule.split()
        print 'dice rule %s %s' % (i, dice_rule)
        for titletuple in product(
            ['four', 'six'],
            ['nw', 'ne', 'sw', 'se'],
            ['1', '2']
        ):
            title = '_'.join(titletuple)
            if title not in dice_rule:
                cut_element(title)

        for letter, prefix in letter_to_prefix.items():
            for suffix in suffixes:
                title = prefix + suffix
                if title != prefix + score_to_suffix[card[letter]]:
                    e = title_to_element[title]
                    e.getparent().remove(e)

        print svg_filename
        fp = file(svg_filename, 'w')
        fp.write(etree.tostring(dom))
        fp.close()

        print cmd
        os.system(cmd)


if not os.path.exists('/tmp/cards'):
    os.makedirs('/tmp/cards')
make_deck(1)
make_deck(2)
make_deck(3)
make_deck(4)
make_blessing_deck()
