#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tall_cards import Card, parse, make_card


class Wind_Beneath_My_Wings(Card):
  desc = u'''
    When you get an advantage that was created by another player,
    you may shuffle a blessing card into your Deckahedron, and they
    may do the same.
    |
    Note, shuffle it into your Deckahedron, you don't put it into
    your discard pile.
    '''



locs = locals()
cards = []
for k, v in locs.items():
    if Card in getattr(v, '__bases__', []):
        cards.append(make_card(v))
