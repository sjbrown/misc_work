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
            retval += '\n' + l
        else:
            retval += ' ' + l

    return retval.strip()

def make_card(C):
    h1 = getattr(C, 'title',
                 # If no 'title', use the class name
                 C.__name__.replace('_', ' '))
    mod = getattr(C, 'mod', '')
    one_check = parse(getattr(C, 'one_check', ''))
    two_check = parse(getattr(C, 'two_check', ''))
    desc_detail = parse(C.desc)
    card = {
        'h1': h1,
        'mod_shield': bool(mod),
        'mod': mod,
        'one_check': one_check,
        'two_check': two_check,
        'desc_detail': desc_detail,
        'circles': getattr(C, 'circles', []),
        'spots': getattr(C, 'spots', []),
    }
    return card


class Hack_and_Slash(Card):
  mod = 'Str'
  one_check = '''
    Deal damage
    and
    enemy attacks you
    '''
  two_check = '''
    Deal damage
    and
    avoid enemy attack
    '''
  desc = u'''
    On a ✔✔, you can choose to expose yourself to the enemy's attack in
    order to deal extra damage
    '''

class Volley(Card):
  mod = 'Dex'
  one_check = '''
    Choose an option
    and
    deal your damage
  '''
  two_check = '''
    Deal your damage
  '''
  desc = u'''
    On a ✗, the GM chooses one:
    |On a ✔, you choose one:
    * You have to move to get the shot, placing you in danger of the GM's choice
    * You have to take what you can get - reduce your damage
    * You have to take several shots - reduce your ammo
  '''

class Parley(Card):
  mod = 'Int'
  one_check = '''
    Provide immediate and
    concrete assurance
    of your promise
  '''
  two_check = '''
    Success
  '''
  desc = u'''
    Using leverage, manipulate an NPC.
    |Leverage is something they need or want.
    |On a ✔✔, they ask you for something and cooperate if you make them a promise first.
    |On a ✗ / ✔, they need some concrete assurance of
    your promise, right now
  '''

class Defy_Danger(Card):
  mod = 'Str/Dex/Int'
  one_check = '''
    Stumble, hesitate
    or flinch
    '''
  two_check = '''
    Success
    '''
  desc = u'''
    When you act despite an imminent threat, say how you deal with it and flip.
    If you do it...
    * by powering through or enduring, flip Str
    * by getting out of the way or acting fast, flip Dex
    * with quick thinking or through mental fortitude, flip Int
    |On a ✗ / ✔, you stumble, hesitate, or flinch: the GM will offer you a worse outcome,
    hard bargain, or ugly choice
  '''

class Defend(Card):
  mod = 'Str'
  one_check = '''
    Place 1 green marker on this tile
  '''
  two_check = '''
    Place 3 green markers on this tile
  '''
  desc = '''
    When you stand in defense of a person, item, or location, you can interfere with attacks against it.
    |So long as you stand in defense, when you or the defended is attacked you may spend
    green markers, 1 for 1, to choose an option:
    * Redirect an attack from the thing you defend to yourself
    * Halve the attack's effect or damage
    * Open up the attacker to an ally giving that ally +1 forward against the attacker
    * Deal damage to the attacker equal to 1 + (number of green cards)
  '''

class Discern_Realities(Card):
  mod = 'Int'
  one_check = '''
    Ask the GM 1
    question from
    the list
    '''
  two_check = '''
    Ask the GM 3
    questions from
    the list
    '''
  desc = '''
    Closely study a situation or person, ask the GM your question(s), and
    take +1 forward when acting on the answers.
    * What happened here recently?
    * What is about to happen?
    * What should I be on the lookout for?
    * What here is useful or valuable to me?
    * Who's really in control here?
    * What here is not what it appears to be
    '''

class Spout_Lore(Card):
  mod = 'Int'
  one_check = '''
    GM tells you
    something interesting
    '''
  two_check = '''
    GM tells you
    something interesting
    and useful
    '''
  desc = u'''
    Consult your accumulated knowledge about something.
    |On a ✔✔ the GM will tell you something interesting and useful about the subject
    relevant to your situation.
    |On a ✗ / ✔ the GM will only tell you something interesting - it's on you to make it useful.
    |On a ✗, the GM will ask you "How do you know this?".
    '''

class Aid_or_Interfere(Card):
  mod = 'Bond'
  one_check = '''
    Target takes +1 or -2
    |(your choice)
    |You are exposed to cost,
    retribution, or danger
    '''
  two_check = '''
    Target takes +1 or -2
    |(your choice)
    '''
  desc = '''
    Help or hinder someone you have a Bond with.
    '''

class And_this_is_for(Card):
  title = 'And this is for...'
  mod = 'Dex'
  one_check = '''
    Deal 1 damage.
    '''
  two_check = '''
    Deal 1d4 damage.
    '''
  desc = '''
    After successfully striking a foe in melee, add a punch,
    kick, or shove.
    '''
  circles = ['all_se']

class Good_Cardio(Card):
  mod = 'Str'
  two_check = '''
    Recover 1d4 exhaustion.
  '''
  one_check = '''
    Recover 1d4 exhaustion.
    |Your foe moves to a position of advantage.
  '''
  one_x = '''
    Recover 1 exhaustion.
    |Your foe moves to a position of advantage.
  '''
  two_x = '''
    Your foe moves to a position of advantage.
  '''
  desc = '''
    Just a momentary pause and you're back in the action.
    |When you would normally lose a Stamina Point from physical exhaustion, you
    can choose to put an exhaustion token on this card instead.
  '''
  spots = {0: ['EX'], 1: ['EX'], 3: ['EX']}
  circles = ['all_ne']

class Tough_Stuff(Card):
  mod = ''
  one_check = '''
    -
  '''
  two_check = '''
    -
  '''
  desc = '''
    When you would normally take physical harm, you can choose to put a
    harm token on this card instead.
  '''
  spots = {0: ['BR'], 1: ['BR'], 3: ['BR']}
  circles = ('all_nw', 'fighter_e')

class Where_It_Hurts(Card):
  mod = ''
  one_check = '''
    -
  '''
  two_check = '''
    -
  '''
  desc = '''
    Turn 1 EX into 1 BR when you deal damage with your weapon.
    Upgrade levels: 2 for 2, 3 for 3.
    '''
  circles = ('all_sw', 'fighter_e')


locs = locals()
cards = []
for k, v in locs.items():
    if Card in getattr(v, '__bases__', []):
        cards.append(make_card(v))
