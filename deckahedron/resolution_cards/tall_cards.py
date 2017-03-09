#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from collections import defaultdict, OrderedDict

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

def make_card(h1, mod_type='', desc_79='', desc_10='', desc_detail='', class_pos=None):
    desc_detail = parse(desc_detail)
    desc_79 = parse(desc_79)
    desc_10 = parse(desc_10)
    card = {
        'h1': h1,
        'mod_shield': bool(mod_type),
        'mod': mod_type,
        'desc_79': desc_79,
        'desc_10': desc_10,
        'label_79': bool(desc_79),
        'label_10': bool(desc_10),
        'desc_detail': desc_detail,
        'class_pos': class_pos,
    }
    return card

cards = [

# ['h1', 'mod',
# '''
# 79
# ''',
# '''
# 10
# ''',
# '''
# detail
# ''',
# 'class_pos',
#  ],

 ['Hack and Slash', 'Str',
'''
Deal damage
and
enemy attacks you
''',
'''
Deal damage
and
avoid enemy attack
''',
'''
On a 10+, you can choose to expose yourself to the enemy's attack in
order to deal extra damage
''',
 ],
 ['Volley', 'Dex',
'''
Choose an option
and
deal your damage
''',
'''
Deal your damage
''',
'''
On a 7-9, choose one:
* You have to move to get the shot, placing you in danger of the GM's choice
* You have to take what you can get - reduce your damage
* You have to take several shots - reduce your ammo
''',
 ],
 ['Parley', 'Int',
'''
Provide immediate and
concrete assurance
of your promise
''',
'''
Success
''',
'''
Using leverage, manipulate an NPC.
Leverage is something they need or want.  On a 7+ they ask you for something and do
it if you make them a promise first. On a 7-9, they need some concrete assurance of
your promise, right now
''',
 ],
 ['Defy Danger', '',
'''
Stumble, hesitate
or flinch
''',
'''
Success
''',
'''
When you act despite an imminent threat, say how you deal with it and roll.
If you do it...
* by powering through or enduring, roll +Str
* by getting out of the way or acting fast, roll +Dex
* with quick thinking or through mental fortitude, roll +Int
|On a 7-9, you stumble, hesitate, or flinch: the GM will offer you a worse outcome, hard bargain, or ugly choice
''',
 ],
 ['Defend', 'Str',
'''
Gain 1 hold
''',
'''
Gain 3 hold
''',
'''
When you stand in defense of a person, item, or location, you can interfere with attacks against it.
So long as you stand in defense, when you or the defended is attacked you may spend hold, 1 for 1, to choose an option:
* Redirect an attack from the thing you defend to yourself
* Halve the attack's effect or damage
* Open up the attacker to an ally giving that ally +1 forward against the attacker
* Deal damage to the attacker equal to your level

''',
 ],
 ['Discern Realities', 'Int',
'''
Ask the GM 1
question from
the list
''',
'''
Ask the GM 3
questions from
the list
''',
'''
Closely study a situation or person, ask the GM your question(s), and
take +1 forward when acting on the answers.
* What happened here recently?
* What is about to happen?
* What should I be on the lookout for?
* What here is useful or valuable to me?
* Who's really in control here?
* What here is not what it appears to be
''',
 ],
 ['Spout Lore', 'Int',
'''
GM tells you
something interesting
''',
'''
GM tells you
something interesting
and useful
''',
'''
Consult your accumulated knowledge about something.
On a 10+ the GM will tell you something interesting and useful about the subject
relevant to your situation.
On a 7-9 the GM will only tell you something interesting - it's on you to make it useful.
The GM might ask you "How do you know this?".
''',
 ],
 ['Aid or Interfere', 'Bond',
'''
Target takes +1 or -2
|(your choice)
|You are exposed to cost,
retribution, or danger
''',
'''
Target takes +1 or -2
|(your choice)
''',
'''
Help or hinder someone you have a Bond with.
''',
 ],

 ['And this is for...', 'Dex',
'''
Deal 1 damage.
''',
'''
Deal 1d4 damage.
''',
'''
After successfully striking a foe in melee, add a punch,
kick, or shove.
''',
['fighter_se'],
 ],

 ['Good Cardio', 'Str',
'''
Recover 1d4 exhaustion.
|Your foe moves to a position of advantage.
''',
'''
Recover 1d4 exhaustion.
''',
'''
Just a momentary pause and you're back in the action.
Spot for 1, 2 or 3 EX.
''',
['fighter_ne'],
 ],

 ['Tough Stuff', '',
'''
-
''',
'''
-
''',
'''
Spot for 1, 2 or 3 BR.
''',
('fighter_nw', 'fighter_e'),
 ],

 ['Where it hurts', '',
'''
-
''',
'''
-
''',
'''
Turn 1 EX into 1 BR when you deal damage with your weapon.
Upgrade levels: 2 for 2, 3 for 3.
''',
('fighter_sw', 'fighter_e'),
 ],

]

cards = [make_card(*x) for x in cards]
