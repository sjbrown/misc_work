#! /usr/bin/env python

import os
from PIL import Image
from datetime import datetime

from . import core
from . import objects

user = None
game = None

def main():
    now_str = datetime.now().strftime('%Y-%m-%d-%H-%M')
    user = objects.User()
    game = objects.Game('Game-%s' % now_str)

    back = Image.open('/tmp/cards/back.png')
    print back.size
    print back.size[0] == back.size[1]

