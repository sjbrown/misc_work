#! /usr/bin/env python

x=[8,4,6,2]; a = [1]*x[0] + [2]*x[1] + [3]*x[2] + [4]*x[3]
x=[5,6,5,4]; b = [1]*x[0] + [2]*x[1] + [3]*x[2] + [4]*x[3]
x=[4,5,6,5]; c = [1]*x[0] + [2]*x[1] + [3]*x[2] + [4]*x[3]
x=[2,6,4,8]; d = [1]*x[0] + [2]*x[1] + [3]*x[2] + [4]*x[3]

cards = [
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 1, 'c': 1, 'd': 1, 'crit_fail': True},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 2, 'c': 4, 'd': 1},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 2, 'c': 3, 'd': 2},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 4, 'c': 3, 'd': 4},
 {'Pro': True,  'Tmark': False, 'a': 2, 'b': 2, 'c': 3, 'd': 4},
 {'Pro': True,  'Tmark': False, 'a': 2, 'b': 3, 'c': 2, 'd': 3},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 1, 'c': 2, 'd': 3},
 {'Pro': False, 'Tmark': False, 'a': 2, 'b': 1, 'c': 2, 'd': 3},
 {'Pro': False, 'Tmark': False, 'a': 2, 'b': 2, 'c': 1, 'd': 2},
 {'Pro': False, 'Tmark': False, 'a': 3, 'b': 1, 'c': 2, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 4, 'b': 4, 'c': 4, 'd': 4, 'crit_win': True},
 {'Pro': False, 'Tmark': True, 'a': 1, 'b': 3, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 3, 'c': 4, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 1, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 1, 'b': 2, 'c': 2, 'd': 4},
 {'Pro': True,  'Tmark': True, 'a': 3, 'b': 2, 'c': 1, 'd': 4},
 {'Pro': True,  'Tmark': True, 'a': 1, 'b': 4, 'c': 4, 'd': 2},
 {'Pro': True,  'Tmark': True, 'a': 3, 'b': 4, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 4, 'b': 3, 'c': 4, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 3, 'c': 1, 'd': 3},
]

def flip(deck):
    new_deck = deck[:]
    random.shuffle(new_deck)
    res = new_deck.pop()
    return res, new_deck

def one_flip(deck):
    return flip(deck)[0]

def two_flip(deck):
    a, deck = flip(deck)
    b, deck = flip(deck)
    return a, b

def three_flip(deck):
    a, deck = flip(deck)
    b, deck = flip(deck)
    c, deck = flip(deck)
    return a, b, c

def contest_results(deck_a, deck_b, flip_fn_a, flip_fn_b):
    return flip_fn_a(deck_a), flip_fn_b(deck_b)

def resolve_contest(deck_a, deck_b, mod_a=0, mod_b=0):
    fns = {
        -2: lambda deck: min(three_flip(deck)),
        -1: lambda deck: min(two_flip(deck)),
         0: lambda deck: one_flip(deck),
         1: lambda deck: max(two_flip(deck)),
         2: lambda deck: max(three_flip(deck)),
    }
    a = fns[mod_a](deck_a)
    b = fns[mod_b](deck_b)
    return cmp(a, b)

def resolve_contest_notie(deck_a, deck_b, mod_a=0, mod_b=0):
    result = resolve_contest(deck_a, deck_b, mod_a, mod_b)
    while result == 0:
        result = resolve_contest(deck_a, deck_b, mod_a, mod_b)
    return result
