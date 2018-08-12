#! /usr/bin/env python

import os
from PIL import Image
from datetime import datetime

import core
import objects

user = None
game = None

def main():
    now_str = datetime.now().strftime('%Y-%m-%d-%H-%M')
    user = objects.User()
    game = objects.Game(user, 'Game-%s' % now_str)

    game.make_poker_deck('/tmp/cards_v0.88/move_deck')
    game.make_poker_deck('/tmp/cards_v0.88/level_deck')
    game.make_poker_deck('/tmp/cards_v0.88/mundane_deck')
    game.make_poker_deck('/tmp/cards_v0.88/magic_deck')
    game.make_booklet('/tmp/cards_v0.88/booklet')
    game.make_square_deck('/tmp/cards')

if __name__ == '__main__':

    main()
