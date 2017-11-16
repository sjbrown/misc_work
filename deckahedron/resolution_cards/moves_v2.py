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

class Isnt_That_Right(Card):
  desc = u'''
    When you're trying to deceive, flimflam, or rook an NPC,
    ask another PC to corroborate your story or otherwise engage
    in the conversation.
    |
    Take the top card of your Deckahedron, but don't flip it or
    show it to anyone. The corroborating player does the same thing.
    You go first. Freely choose which side of this card you are going to
    flip, and say the side, but not the result.
    The corroborating player does the same thing, each of you only saying
    one word and nothing else.
    Both of you flip your cards simultaneously.
    |
    If the results match, your deception succeeds flawlessly.
    |
    If the results are the same color, choose between suspicion, cost,
    or limited progress.
    |
    If one result shows ✗s and the other shows ✔s, the NPC's suspicion
    increases and the GM makes a move.
    |
    To apply advantage to this move, just draw two cards,
    and discard one before you say which side you are going to flip.
    '''



locs = locals()
cards = []
for k, v in locs.items():
    if Card in getattr(v, '__bases__', []):
        cards.append(make_card(v))
