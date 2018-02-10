#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import sys
import string
from pprint import pprint, pformat
from tall_cards import cards

from svg_dom import DOM, export_png, export_tall_png

DEBUG = 1

def filenamify(s):
    x = s.lower()
    l = [c for c in x if c in (' ' + string.ascii_lowercase)]
    x = ''.join(l)
    x = x.replace(' ', '_')
    return x


def filter_dom_elements(dom, card):
    cut_these = [
      'spacer',
      'mod_str', 'mod_int', 'mod_dex', 'mod_bond',
      'mod_str/dex/int', 'mod_int/dex', 'mod_dex/str',
      'wiz_ne', 'wiz_e', 'wiz_se', 'wiz_sw', 'wiz_w', 'wiz_nw',
      'rogue_ne', 'rogue_e', 'rogue_se', 'rogue_sw', 'rogue_w', 'rogue_nw',
      'fighter_ne', 'fighter_e', 'fighter_se', 'fighter_sw', 'fighter_w', 'fighter_nw',
      'all_ne', 'all_e', 'all_se', 'all_sw', 'all_w', 'all_nw',
      'spot_level_0', 'spot_level_g1', 'spot_level_g2',
      'spot_1_1', 'spot_2_1', 'spot_3_1',
      'spot_1_2', 'spot_2_2', 'spot_3_2',
      'level_r3', 'level_r2', 'level_r1',
      'level_0', 'level_g1', 'level_g2',
      'level_start_r3', 'level_start_r2', 'level_start_r1',
      'level_start_0', 'level_start_g1', 'level_start_g2',
      'spot_level_start_0', 'spot_level_start_g1', 'spot_level_start_g2',
      'C', 'CC/F', 'CC/W', 'CC/R',
    ]
    card_spots = card.get('spots') or {}
    has_card_spots = any(card_spots[x] for x in card_spots)
    checks = [
        x for x in [card.get('x_check'), card.get('one_x'),
                    card.get('one_check'), card.get('two_check')]
        if x not in (None, '')
    ]
    if has_card_spots:
        for key in dom.layers:
            if 'spot_' in key:
                dom.layer_show(key)
            elif 'std_' in key:
                dom.layer_hide(key)

        cut_these.remove('spot_level_0')
        cut_these.remove('spot_level_g1')
        cut_these.remove('spot_level_g2')

        if len(checks) == 0:
            dom.layer_hide('spot_3lines')
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
            dom.layer_hide('spot_x_check')
            dom.layer_hide('spot_one_check')
            dom.layer_hide('spot_two_check')
        else:
            raise ValueError('Spots! %s' % pformat(card))

        for i in range(3):
            if '1' in card.get('spots')[i]:
                cut_these.remove('spot_%s_1' % (i+1))
            if '2' in card.get('spots')[i]:
                cut_these.remove('spot_%s_2' % (i+1))
            if 'EX' in card.get('spots')[i]:
                dom.layer_hide('spot_br')
            if 'BR' in card.get('spots')[i]:
                dom.layer_hide('spot_ex')

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
        if card.get('equipment') and 'equipment' in key:
            dom.layer_show(key)
        elif 'equipment' in key:
            dom.layer_hide(key)

        if 'more_power' in key:
            dom.layer_hide(key)
            if card.get('title','').lower() in [
                '____ of unerring dispatch',
                '____ of vitality',
                '____ bow',
                '____ sword',
            ]:
                dom.layer_show(key)

        if card.get('reqs') and 'reqs' in key:
            dom.layer_show(key)
        elif 'reqs' in key:
            dom.layer_hide(key)

        if card.get('tags') and 'tags' in key:
            dom.layer_show(key)
        elif 'tags' in key:
            dom.layer_hide(key)

        if card.get('flags') and 'flags' in key:
            dom.layer_show(key)
        elif 'flags' in key:
            dom.layer_hide(key)

        if card.get('circles') and 'class_' in key:
            dom.layer_show(key)

        if len(checks) == 0:
            if '_2lines' in key or '_3lines' in key:
                dom.layer_hide(key)
        elif len(checks) == 2:
            if '_0lines' in key or '_3lines' in key:
                dom.layer_hide(key)
        elif len(checks) == 3:
            if '_0lines' in key or '_2lines' in key:
                dom.layer_hide(key)
#
#        if card.get('one_x'):
#            if '_2lines' in key:
#                dom.layer_hide(key)
#        else:
#            if '_3lines' in key:
#                dom.layer_hide(key)

        if 'levels' in key and not card.get('level_start'):
            dom.layer_hide(key)

    if card.get('level_start'):
        if has_card_spots and checks:
            cut_these.remove('spot_level_start_' + card['level_start'])
        else:
            cut_these.remove('level_start_' + card['level_start'])

    if card.get('reqs'):
        cut_these.remove(card['reqs'])

    if card.get('levels'):
        [cut_these.remove('level_' + lvl) for lvl in card['levels']]

    if card.get('circles'):
        [cut_these.remove(x) for x in card['circles']]
    if card.get('attr'):
        keep = 'mod_' + card['attr'].lower()
        print keep
        cut_these.remove(keep)
    else:
        cut_these.append('mod_shield')

    for x in cut_these:
        dom.cut_element(x)



def one_blank_3lines_front():
    dom = DOM('tall_card_front.svg')

    filter_dom_elements(dom, {})
    dom.replace_text('words_one_x', '')
    dom.replace_text('words_one_check', '')
    dom.replace_text('words_two_check', '')
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
          '2lines' in key
          or
          'spot' in key
        ):
            dom.layer_hide(key)
        elif '3lines' in key:
            dom.layer_show(key)

    # Create the svg file and export a PNG
    svg_filename = '/tmp/tall_cards/deck_card_face_3lines.svg'
    png_filename = '/tmp/tall_cards/deck_card_face_3lines.png'
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

    if card.get('flags'):
        flags_text = ','.join(card['flags'])
        dom.replace_text('flags_text', flags_text)

    if card.get('tags'):
        tag_text = ','.join(card['tags'])
        dom.replace_text('card_tags_text', tag_text)

    if card.get('one_x'):
        dom.replace_text('words_one_x', card['one_x'], ideal_num_chars=40)
    if card.get('x_check'):
        dom.replace_text('words_left', card['x_check'], ideal_num_chars=30)
        dom.replace_text('spot_words_left', card['x_check'], ideal_num_chars=30)
    elif card.get('one_check'):
        dom.replace_text('words_left', card['one_check'], ideal_num_chars=30)
        dom.replace_text('spot_words_left', card['one_check'], ideal_num_chars=30)
        dom.replace_text('words_one_check', card['one_check'], ideal_num_chars=40)
    else:
        # Card has nothing to do with flips
        dom.replace_text('spot_words_left', '')
        dom.replace_text('words_left', '')
    dom.replace_text('words_right', card['two_check'], ideal_num_chars=20)
    dom.replace_text('spot_words_right', card['two_check'], ideal_num_chars=20)
    dom.replace_text('words_two_check', card['two_check'], ideal_num_chars=40)

    if card.get('one_x') or card.get('x_check') or card.get('one_check'):
        dom.replace_text('desc_detail', card['desc_detail'],
                         ideal_num_chars=200)
    else:
        dom.replace_text('desc_detail', card['desc_detail'],
                         ideal_num_chars=400)
    dom.replace_h1(card['title'])

    return dom

def custom_card_dom(card):
    tail = filenamify(card['title'])
    fpath = 'tall_card__' + tail + '.svg'
    if os.path.isfile(fpath):
        print 'Found custom card', fpath
        return DOM(fpath)
    return None

def make_deck(cards):
    export_tall_png('tall_card_back2.svg', '/tmp/tall_cards/back.png')
    export_tall_png('equipment_back1.svg', '/tmp/tall_cards/back_equip1.png')
    export_tall_png('equipment_back2.svg', '/tmp/tall_cards/back_equip2.png')
    export_tall_png('tall_card_stats.svg', '/tmp/tall_cards/page_stats.png')
    export_tall_png('tall_card_hints.svg', '/tmp/tall_cards/page_hints.png')

    export_tall_png('level_card_background_anchor.svg', '/tmp/tall_cards/level_background_anchor.png')
    export_tall_png('level_card_eager_learner.svg', '/tmp/tall_cards/level_eager_learner.png')
    export_tall_png('level_card_getting_the_hang.svg', '/tmp/tall_cards/level_getting_the_hang.png')
    export_tall_png('level_card_its_in_here.svg', '/tmp/tall_cards/level_its_in_here.png')
    export_tall_png('level_card_rallying_cry2.svg', '/tmp/tall_cards/level_rallying_cry2.png')
    export_tall_png('level_card_rallying_cry.svg', '/tmp/tall_cards/level_rallying_cry.png')
    export_tall_png('level_card_back.svg', '/tmp/tall_cards/back_level.png')

    one_blank_3lines_front()

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
        svg_filename = '/tmp/tall_cards/face%02d_%s.svg' % (
            (i+1),
            filenamify(card['title'])
        )
        png_filename = '/tmp/tall_cards/face%02d_%s.png' % (
            (i+1),
            filenamify(card['title'])
        )

        dom.write_file(svg_filename)

        export_tall_png(svg_filename, png_filename)

def make_documentation_images(cards):
    tmp_template_filename = '/tmp/tall_cards/move_card_template.svg'
    for i, card in enumerate(cards):
        slug = filenamify(card['title'])
        png_filename = '/tmp/tall_cards/face%02d_%s.png' % ((i+1), slug)
        doc_img_filename = '../images/move_%s.png' % slug
        template_filename = '../images/move_card_template.svg'
        if os.path.isfile(doc_img_filename):
            c = file(template_filename).read()
            c = re.sub(
              'xlink:href="file://.*.png"',
              'xlink:href="file://%s"' % png_filename,
              c
            )
            outfile = file(tmp_template_filename, 'w')
            outfile.write(c)
            outfile.close()

            export_png(tmp_template_filename, doc_img_filename, 381, 381)


def make_deck_from_svg_dir(dirpath, fpart=None):
    for fname in os.listdir(dirpath):
        if fname.endswith('.svg'):
            if fpart and fpart not in fname:
                continue
            base = os.path.splitext(fname)[0]
            png_filename = '/tmp/tall_cards/%s.png' % base
            export_tall_png(dirpath + '/' +fname, png_filename)


if __name__ == '__main__':
    if not os.path.exists('/tmp/tall_cards'):
        os.makedirs('/tmp/tall_cards')

    import parse_cards_csv

    if len(sys.argv) > 1:
        card_grep = sys.argv[1]
        filtered = cards + parse_cards_csv.get_objs(card_grep)
        if DEBUG:
            print 'filtering for', card_grep
        filtered = [c for c in filtered
          if card_grep.lower() in c['title'].lower()]
    else:
        filtered = cards + parse_cards_csv.get_objs()

    make_deck(filtered)
    make_documentation_images(filtered)
