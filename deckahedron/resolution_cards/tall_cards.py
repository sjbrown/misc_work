#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from collections import defaultdict, OrderedDict

class Card:
    pass

def parse(s):
    retval = ''
    for line in s.split('\n'):
        l = line.strip()
        if not l:
            continue
        if l.startswith('|'):
            retval += '\n' + l[1:]
        elif l.startswith('*'):
            retval += '\n' + u'✷' + l[1:]
        else:
            retval += ' ' + l

    return retval.strip()

def make_card(C):
    title = getattr(C, 'title',
                 # If no 'title', use the class name
                 C.__name__.replace('_', ' '))
    attr = getattr(C, 'attr', '')
    one_x = parse(getattr(C, 'one_x', ''))
    x_check = parse(getattr(C, 'x_check', ''))
    one_check = parse(getattr(C, 'one_check', ''))
    two_check = parse(getattr(C, 'two_check', ''))
    desc_detail = parse(C.desc)
    if getattr(C, 'levels', []):
        levels = C.levels
    else:
        if getattr(C, 'level_start', None):
            levels = ['r3', 'r2', 'r1', '0', 'g1', 'g2']
        else:
            levels = []

    card = {
        'title': title,
        'attr_shield': bool(attr),
        'attr': attr,
        'one_x': one_x,
        'x_check': x_check,
        'one_check': one_check,
        'two_check': two_check,
        'desc_detail': desc_detail,
        'circles': getattr(C, 'circles', []),
        'spots': getattr(C, 'spots', {}),
        'levels': levels,
        'level_start': getattr(C, 'level_start', None),
    }
    return card


class Hack_and_Slash(Card):
  attr = 'Str'
  one_x = '''
    1 attack power and the foe attacks you
  '''
  one_check = '''
    Roll attack power and the foe attacks you
    '''
  two_check = '''
    Roll attack power and choose
    '''
  desc = u'''
    On a ✔✔, you can choose:
    * Avoid the foe's attack
    * Expose yourself to the foe's attack in order to deal extra attack power
    '''

class Volley(Card):
  attr = 'Dex'
  one_x = '''
    Roll attack power.
    GM chooses an option.
  '''
  one_check = '''
    Roll attack power.
    Choose an option
  '''
  two_check = '''
    Roll attack power.
  '''
  desc = u'''
    Send a volley flying with your ranged weapon.
    |
    Choices:
    * You have to move to get the shot, placing you in danger of the GM's choice
    * You have to take what you can get - halve your attack power
    * You have to take several shots - lose 1 Equipment point
  '''
  level_start = '0'
  levels = ['0', 'g1']

class Parley(Card):
  attr = 'Int'
  x_check = '''
    Provide immediate and
    concrete assurance
    of your promise
  '''
  two_check = '''
    Make a promise and get what you want.
  '''
  desc = u'''
    Using leverage, manipulate an NPC. "Leverage" is something they need or want.
    |
    On a ✔✔, they ask you for something and cooperate if you make them a promise first.
    |
    On a ✗ / ✔, they need some concrete assurance of your promise, right now
    |
    |
    If you don't have leverage, flip with 1 level of disadvantage.
  '''
  level_start = '0'
  levels = ['0', 'g1']

class Defy_Danger(Card):
  attr = 'Str/Dex/Int'
  one_check = '''
    You do it, but there's a new complication
    '''
  one_x = '''
    Make progress, but stumble, hesitate, or flinch.
    '''
  two_check = '''
    Success
    '''
  desc = u'''
    When you act despite an imminent threat, say how you deal with it and flip.
    |
    If you do it...
    * by powering through or enduring, flip Str
    * by getting out of the way or acting fast, flip Dex
    * with quick wits or through mental fortitude, flip Int
    |
    |
    On a ✗ / ✔, the GM may ask you a question, offer you a worse outcome, hard bargain, or ugly choice
  '''

class Defend(Card):
  attr = 'Str'
  one_x = '''
    Place 1 green marker on this card
  '''
  one_check = '''
    Place 2 green markers on this card
  '''
  two_check = '''
    Place 3 green markers on this card
  '''
  desc = '''
    When you stand in defense of a person, item, or location, you can interfere with attacks against it.
    |
    So long as you stand in defense, when you or the defended is attacked you may spend
    green markers, 1 for 1, to choose an option:
    * Redirect an attack from the thing you defend to yourself
    * Halve the attack's effect or damage
    * Open up the attacker to an ally giving that ally a +1 advantage against the attacker
    * Deal 1 attack power against the attacker
  '''

class Discern_Realities(Card):
  attr = 'Int'
  one_x = '''
    Ask the GM 1
    question from
    the list
    '''
  one_check = '''
    Ask the GM 2
    questions from
    the list
    '''
  two_check = '''
    Ask the GM 3
    questions from
    the list
    '''
  desc = '''
    Closely study a situation or person, ask the GM your question(s), and
    gain a +1 advantage when acting on the answers.
    * What happened here recently?
    * What is about to happen?
    * What should I be on the lookout for?
    * What here is useful or valuable to me?
    * Who's really in control here?
    * What here is not what it appears to be
    '''

class Spout_Lore(Card):
  attr = 'Int'
  x_check = '''
    The GM tells you something interesting
    - it's on you to make it useful.
    '''
  two_check = '''
    The GM tells you something interesting
    and useful about the subject relevant to your situation
    '''
  desc = u'''
    Consult your accumulated knowledge about something.
    |
    |
    On a ✗, the GM may ask you "How do you know this?".
    '''



locs = locals()
cards = []
for k, v in locs.items():
    if Card in getattr(v, '__bases__', []):
        cards.append(make_card(v))
