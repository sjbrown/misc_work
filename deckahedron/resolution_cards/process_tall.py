#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import sys
from pprint import pprint, pformat
from tall_cards import cards

from svg_dom import DOM, export_tall_png

DEBUG = 1


def filter_dom_elements(dom, card):
    cut_these = [
      'mod_str', 'mod_int', 'mod_dex', 'mod_bond',
      'mod_str/dex/int', 'mod_int/dex', 'mod_dex/str',
      'wiz_ne', 'wiz_e', 'wiz_se', 'wiz_sw', 'wiz_w', 'wiz_nw',
      'rogue_ne', 'rogue_e', 'rogue_se', 'rogue_sw', 'rogue_w', 'rogue_nw',
      'fighter_ne', 'fighter_e', 'fighter_se', 'fighter_sw', 'fighter_w', 'fighter_nw',
      'all_ne', 'all_e', 'all_se', 'all_sw', 'all_w', 'all_nw',
      'spot_level_0', 'spot_level_g1', 'spot_level_g2',
      'level_r3', 'level_r2', 'level_r1',
      'level_0', 'level_g1', 'level_g2',
      'level_start_r3', 'level_start_r2', 'level_start_r1',
      'level_start_0', 'level_start_g1', 'level_start_g2',
      'spot_level_start_0', 'spot_level_start_g1', 'spot_level_start_g2',
    ]
    if card.get('spots'):
        for key in dom.layers:
            if 'spot_' in key:
                dom.layer_show(key)
            elif 'std_' in key:
                dom.layer_hide(key)

        cut_these.remove('spot_level_0')
        cut_these.remove('spot_level_g1')
        cut_these.remove('spot_level_g2')

        checks = [
            x for x in [card.get('x_check'), card.get('one_x'),
                        card.get('one_check'), card.get('two_check')]
            if x not in (None, '')
        ]
        if len(checks) == 0:
            dom.layer_hide('spot_3lines')
            dom.layer_hide('spot_2lines')
            dom.layer_hide('spot_x_check')
            dom.layer_hide('spot_one_check')
            dom.layer_hide('spot_two_check')
        elif len(checks) == 2:
            dom.layer_hide('spot_3lines')
            if not card.get('x_check'):
                dom.layer_hide('spot_x_check')
            if not card.get('one_check'):
                dom.layer_hide('spot_one_check')
            if not card.get('two_check'):
                dom.layer_hide('spot_two_check')
        elif len(checks) == 3:
            dom.layer_hide('spot_2lines')
            dom.layer_hide('spot_x_check')
            dom.layer_hide('spot_one_check')
            dom.layer_hide('spot_two_check')
        else:
            raise ValueError('Spots! %s' % pformat(card))

        if card.get('spots')[0][0].upper() == 'EX':
            dom.layer_hide('spot_br')
        elif card.get('spots')[0][0].upper() == 'BR':
            dom.layer_hide('spot_ex')
        else:
            raise ValueError('Spots? %s' % card.get('spots'))

    else:
        for key in dom.layers:
            if 'spot_' in key:
                dom.layer_hide(key)
            elif 'std_' in key:
                dom.layer_show(key)
            if not card.get('x_check') and 'x_check' in key:
                dom.layer_hide(key)
            if not card.get('one_check') and 'one_check' in key:
                dom.layer_hide(key)
            if not card.get('two_check') and 'two_check' in key:
                dom.layer_hide(key)

    for key in dom.layers:
        if card.get('one_x'):
            if '_2lines' in key:
                dom.layer_hide(key)
        else:
            if '_3lines' in key:
                dom.layer_hide(key)

        if not card.get('level_start') and 'levels' in key:
            dom.layer_hide(key)

    if card.get('level_start'):
        if card.get('spots'):
            cut_these.remove('spot_level_start_' + card['level_start'])
        else:
            cut_these.remove('level_start_' + card['level_start'])
    if card.get('levels'):
        [cut_these.remove('level_' + lvl) for lvl in card['levels']]

    if card.get('circles'):
        print card['circles']
        [cut_these.remove(x) for x in card['circles']]
    if card.get('attr'):
        keep = 'mod_' + card['attr'].lower()
        print keep
        cut_these.remove(keep)
    else:
        cut_these.append('mod_shield')
    for x in cut_these:
        dom.cut_element(x)



def one_blank_front():
    dom = DOM('tall_card_front.svg')

    print '\nWorking on Blank Front card'
    print '\n'

    filter_dom_elements(dom, {})
    dom.replace_text('words_left', '')
    dom.replace_text('spot_words_left', '')
    dom.replace_text('words_right', '')
    dom.replace_text('spot_words_right', '')
    dom.replace_text('desc_detail', '')
    dom.replace_h1('')
    for key in dom.layers:
        if (
          'x_check' in key
          or
          'one_check' in key
          or
          'two_check' in key
          or
          'std_3lines' in key
        ):
            dom.layer_hide(key)

    # Create the svg file and export a PNG
    svg_filename = '/tmp/tall_cards/deck_card_face_blank.svg'
    png_filename = '/tmp/tall_cards/deck_card_face_blank.png'
    dom.write_file(svg_filename)
    export_tall_png(svg_filename, png_filename)


def make_card_dom(card):
    dom = DOM('tall_card_front.svg')

    if DEBUG:
        print '\nWorking on ' + card['title']
        print '\n'
        pprint(card)

    if card.get('levels') and not card.get('level_start'):
        raise Exception("Levels only works with level_start")

    filter_dom_elements(dom, card)
    if card.get('one_x'):
        dom.replace_text('words_one_x', card['one_x'], max_chars=60)
    if card.get('x_check'):
        dom.replace_text('words_left', card['x_check'], max_chars=40)
        dom.replace_text('spot_words_left', card['x_check'], max_chars=40)
    elif card.get('one_check'):
        dom.replace_text('words_left', card['one_check'], max_chars=40)
        dom.replace_text('spot_words_left', card['one_check'], max_chars=40)
        dom.replace_text('words_one_check', card['one_check'], max_chars=60)
    else:
        # Card has nothing to do with flips
        dom.replace_text('spot_words_left', '')
        dom.replace_text('words_left', '')
    dom.replace_text('words_right', card['two_check'], max_chars=40)
    dom.replace_text('spot_words_right', card['two_check'], max_chars=40)
    dom.replace_text('words_two_check', card['two_check'], max_chars=60)
    dom.replace_text('desc_detail', card['desc_detail'], max_chars=300)
    dom.replace_h1(card['title'])

    return dom

def custom_card_dom(card):
    words = card['title'].split()
    tail = '_'.join([x.lower() for x in words])
    fpath = 'tall_card__' + tail + '.svg'
    if os.path.isfile(fpath):
        print 'Found custom card', fpath
        return DOM(fpath)
    return None

def make_deck(cards):
    export_tall_png('tall_card_back.svg', '/tmp/tall_cards/back.png')

    #one_blank_front()

    for i, card in enumerate(cards):
        try:
            dom = custom_card_dom(card)
            if not dom:
                dom = make_card_dom(card)
        except:
            print 'FAIL'
            print 'card:'
            pprint(card)
            raise

        # Create the svg file and export a PNG
        svg_filename = '/tmp/tall_cards/deck_card_face%02d.svg' % ((i+1))
        png_filename = '/tmp/tall_cards/deck_card_face%02d.png' % ((i+1))

        dom.write_file(svg_filename)

        export_tall_png(svg_filename, png_filename)


if __name__ == '__main__':
    if not os.path.exists('/tmp/tall_cards'):
        os.makedirs('/tmp/tall_cards')

    import parse_moves_csv

    filtered = cards + parse_moves_csv.get_objs()
    if len(sys.argv) > 1:
        card_grep = sys.argv[1]
        if DEBUG:
            print 'filtering for', card_grep
        filtered = [c for c in filtered
          if card_grep.lower() in c['title'].lower()]

    make_deck(filtered)
