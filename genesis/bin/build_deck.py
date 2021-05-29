#! /usr/bin/env python2

import os
import re
import sys
import shutil

from version import VERSION

carddir = '/tmp/genesis'+VERSION
outdir = './build/'

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


    def build(filenames, build_dir):
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir)
        name_pattern = 'card_tts_%02d.png'
        for (i,fname) in enumerate(filenames):
            i += 1
            print('copying %s' % fname)
            shutil.copy(
              carddir + '/' + fname,
              build_dir + '/' + name_pattern % i
            )

        deck_svg_fname = build_dir + '/deck_' + deckname + '.svg'
        deck_png_fname = build_dir + '/deck_' + deckname + '.png'
        shutil.copy('./deck_template_tts_7x10.svg', deck_svg_fname)
        export_png(deck_svg_fname, deck_png_fname, 3969, 3789)
        return deck_png_fname

    deck_build_dir = carddir + '/build_deck_' + sys.argv[1]
    faces_png_fname = build(card_faces_filenames, deck_build_dir)
    shutil.copy(
      faces_png_fname,
      outdir + '/deck_faces_' + sys.argv[1] + '.png'
    )

    if len(card_backs_filenames) == 0:
        print('Skipping card backs (none provided)')
    elif len(card_backs_filenames) == 1:
        shutil.copy(
          carddir + '/' + card_backs_filenames[0],
          outdir + '/deck_backs_' + sys.argv[1] + '.png'
        )
    else:
        deck_build_dir = carddir + '/build_deck_back_' + sys.argv[1]
        backs_png_fname = build(card_backs_filenames, deck_build_dir)
        shutil.copy(
          backs_png_fname,
          outdir + '/deck_backs_' + sys.argv[1] + '.png'
        )

