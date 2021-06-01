#! /usr/bin/env python2

import os
import re
import sys
import shutil
from collections import defaultdict

from version import VERSION

carddir = '/tmp/genesis'+VERSION
outdir = './build/'

class GroupIntoNines:
    count = 0
    def __call__(self):
        self.count += 1
        return int((self.count-1)/9)

def run(cmd):
    if os.environ.get('DEBUG'):
        print(cmd)
    os.system(cmd)

def ensure_dirs(filepath):
    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

def export_png(svg, png, width, height):
    ensure_dirs(png)
    cmd_fmt = 'inkscape --export-png=%s --export-width=%s --export-height=%s %s'
    cmd = cmd_fmt % (png, width, height, svg)
    run(cmd)

def export_pdf(svg, pdf):
    ensure_dirs(pdf)
    cmd_fmt = 'inkscape --export-pdf=%s %s'
    cmd = cmd_fmt % (pdf, svg)
    run(cmd)


if __name__ == '__main__':
    if not os.environ['PWD'].endswith('genesis'):
        print('This must be run from the genesis directory')
        sys.exit(1)

    deckname = sys.argv[1]
    if not deckname:
        print('Provide the name of the deck as the first argument!')
        sys.exit(1)

    card_faces_filenames = [x for x in os.listdir(carddir)
        if (deckname in x)
        and (x.startswith('card_rect'))
        and (x.endswith('.png'))
        and ('back' not in x)
    ]
    card_faces_filenames.sort()
    card_backs_filenames = [x for x in os.listdir(carddir)
        if (deckname in x)
        and (x.startswith('card_rect'))
        and (x.endswith('.png'))
        and ('back' in x)
    ]
    card_backs_filenames.sort()

    def build_tts(filenames, build_dir, prefix):
        for (i,fname) in enumerate(filenames):
            print('tts copying %s' % fname)
            shutil.copy(
              carddir + '/' + fname,
              build_dir + '/card_tts_%02d.png' % (i+1)
            )
        deck_svg_fname = build_dir + '/deck_' + deckname + '.svg'
        deck_png_fname = build_dir + '/deck_' + deckname + '.png'
        shutil.copy('./deck_template_tts_7x10.svg', deck_svg_fname)
        export_png(deck_svg_fname, deck_png_fname, 3969, 3789)
        shutil.copy(
          deck_png_fname,
          outdir + '/' + prefix + deckname + '.png'
        )

    def build_pnp(filenames, build_dir, prefix):
        groups_of_nines = defaultdict(list)
        NinesCounter = GroupIntoNines()

        deck_svg_fname = build_dir + '/deck_pnp_' + deckname + '.svg'
        shutil.copy('./deck_template_pnp_3x3.svg', deck_svg_fname)

        for fname in filenames:
            groups_of_nines[NinesCounter()].append(fname)
        for group_index, nine_filenames in groups_of_nines.items():
            run('rm %s/card_3x3*png' % (build_dir))
            for (i,fname) in enumerate(nine_filenames):
                print('pnp copying %s' % fname)
                shutil.copy(
                  carddir + '/' + fname,
                  build_dir + '/card_3x3_%02d.png' % (i+1)
                )
            deck_pdf_fname = '%s/deck_pnp_%s_%s.png' % (
              build_dir, group_index, deckname
            )
            export_pdf(deck_svg_fname, deck_pdf_fname)
            shutil.copy(
              deck_pdf_fname,
              '%s/%s%s_%s.pdf' % (outdir, prefix, deckname, group_index)
            )

    def build(filenames, build_dir, prefix='deck_faces_'):
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir)
        filenames.sort()

        build_tts(filenames, build_dir, prefix)
        build_pnp(filenames, build_dir, prefix)


    deck_build_dir = carddir + '/build_deck_' + sys.argv[1]
    build(card_faces_filenames, deck_build_dir)

    if len(card_backs_filenames) == 0:
        print('Skipping card backs (none provided)')
    elif len(card_backs_filenames) == 1:
        shutil.copy(
          carddir + '/' + card_backs_filenames[0],
          outdir + '/deck_backs_' + sys.argv[1] + '.png'
        )
    else:
        deck_build_dir = carddir + '/build_deck_back_' + sys.argv[1]
        build(card_backs_filenames, deck_build_dir, 'deck_backs_')

