#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import string
from pprint import pprint, pformat
from tall_cards import cards
from process_tall import filenamify
from version import VERSION

from svg_dom import DOM, export_pdf, export_tall_png

SRCDIR = '/tmp/cards_v' + VERSION

DEBUG = 1


if __name__ == '__main__':
    fp = file('print_and_play_move_template.svg')
    template = fp.read()
    fp.close()
    counter = 1

    pngs = [x for x in os.listdir(SRCDIR) if x.endswith('.png')]

    for i, fname in enumerate(sorted(pngs)):
        if (i % 9) == 0:
            copy = str(template)

        copy = copy.replace(
            'cards_v0.86/%d' % ((i%9)+1) + '.png',
            'cards_v' + VERSION + '/' + fname
        )

        if (i % 9) == 8:
            new_fname = '/tmp/print_and_play%02d.svg' % counter
            new_pdf_name = '/tmp/print_and_play%02d.pdf' % counter
            print 'Writing', new_pdf_name
            fp = file(new_fname, 'w')
            fp.write(copy)
            fp.close()
            export_pdf(new_fname, new_pdf_name)
            counter += 1

    fname = 'print_and_play_deckahedron_template.svg'
    new_pdf_name = '/tmp/print_and_play_deckahedron.pdf'
    print 'Writing', new_pdf_name
    export_pdf(fname, new_pdf_name)

