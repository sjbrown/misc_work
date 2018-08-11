#! /usr/bin/env python

import os
from PIL import Image
from datetime import datetime

import core
import objects

user = None
game = None

def process_dir(game, dirpath):
    back_filepath = dirpath + '/back.png'
    back = Image.open(back_filepath)
    if back.size[0] == back.size[1]:
        game.make_square_deck(dirpath)
    else:
        game.make_poker_deck(dirpath)


def main():
    now_str = datetime.now().strftime('%Y-%m-%d-%H-%M')
    user = objects.User()
    game = objects.Game(user, 'Game-%s' % now_str)

    process_dir(game, '/tmp/cards/')

if __name__ == '__main__':

    main()
