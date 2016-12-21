#! /usr/bin/env python

import random
from collections import defaultdict

def pct(x, total):
    return '%2.1f%%' % (100*float(x)/total)

x=[8,4,6,2]; a = [1]*x[0] + [2]*x[1] + [3]*x[2] + [4]*x[3]
x=[5,6,5,4]; b = [1]*x[0] + [2]*x[1] + [3]*x[2] + [4]*x[3]
x=[4,5,6,5]; c = [1]*x[0] + [2]*x[1] + [3]*x[2] + [4]*x[3]
x=[2,6,4,8]; d = [1]*x[0] + [2]*x[1] + [3]*x[2] + [4]*x[3]

cards = [
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 1, 'c': 1, 'd': 1, 'crit_fail': True},
 {'Pro': True,  'Tmark': False, 'a': 1, 'b': 2, 'c': 4, 'd': 1},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 2, 'c': 3, 'd': 2},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 4, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': False, 'a': 2, 'b': 2, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': False, 'a': 2, 'b': 3, 'c': 2, 'd': 3},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 1, 'c': 2, 'd': 3},
 {'Pro': False, 'Tmark': False, 'a': 2, 'b': 1, 'c': 2, 'd': 3},
 {'Pro': True,  'Tmark': False, 'a': 2, 'b': 2, 'c': 1, 'd': 2},
 {'Pro': False, 'Tmark': False, 'a': 3, 'b': 1, 'c': 2, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 4, 'b': 4, 'c': 4, 'd': 4, 'crit_win': True},
 {'Pro': False, 'Tmark': True, 'a': 1, 'b': 3, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 3, 'c': 4, 'd': 2},
 {'Pro': True,  'Tmark': True, 'a': 3, 'b': 1, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 1, 'b': 2, 'c': 2, 'd': 4},
 {'Pro': True,  'Tmark': True, 'a': 3, 'b': 2, 'c': 1, 'd': 4},
 {'Pro': True,  'Tmark': True, 'a': 1, 'b': 4, 'c': 4, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 4, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 4, 'b': 3, 'c': 4, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 3, 'c': 1, 'd': 3},
]

def flip(deck):
    # Takes a card off the deck and returns that new deck
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

def four_flip(deck):
    a, deck = flip(deck)
    b, deck = flip(deck)
    c, deck = flip(deck)
    d, deck = flip(deck)
    return a, b, c, d

def contest_results(deck_a, deck_b, flip_fn_a, flip_fn_b):
    return flip_fn_a(deck_a), flip_fn_b(deck_b)

def resolve_contest(deck_a, deck_b, mod_a=0, mod_b=0):
    fns = {
        -3: lambda deck: min(four_flip(deck)),
        -2: lambda deck: min(three_flip(deck)),
        -1: lambda deck: min(two_flip(deck)),
         0: lambda deck: one_flip(deck),
         1: lambda deck: max(two_flip(deck)),
         2: lambda deck: max(three_flip(deck)),
    }
    a = fns[mod_a](deck_a)
    b = fns[mod_b](deck_b)
    return cmp(a, b)


class Notie(object):
    """
    No ties allowed
    Just re-draw whenever there's a tie.

    This can be really shitty, because (d,d,2,2) or (a,a,-2,-2) can
    result in 1.7x the needed draws to get to a resolution.
    (see analyze_contest_notie)
    This should be reserved only for epic struggles where a prolonged
    stalemate makes a lot of narrative sense.
    """
    ties = 0
    num_contests = 0
    tie_distribution = defaultdict(int)
    @classmethod
    def resolve_contest(cls, deck_a, deck_b, mod_a=0, mod_b=0):
        contest_ties = 0
        cls.num_contests += 1
        result = resolve_contest(deck_a, deck_b, mod_a, mod_b)
        while result == 0:
            contest_ties += 1
            result = resolve_contest(deck_a, deck_b, mod_a, mod_b)
        cls.tie_distribution[contest_ties] += 1
        cls.ties += contest_ties
        return result

    @classmethod
    def clear(cls):
        cls.ties = 0
        cls.num_contests = 0
        cls.tie_distribution = defaultdict(int)

    @classmethod
    def analysis(cls):
        return 'Ties %s (%2.1fx), %s' % (
            cls.ties,
            cls.multiple(),
            {k:pct(v, cls.num_contests) for (k,v) in cls.tie_distribution.items()}
        )

    @classmethod
    def multiple(cls):
        return float(cls.num_contests + cls.ties)/cls.num_contests

def resolve_check(deck, mod=0):
    fns = {
        -3: lambda deck: min(four_flip(deck)),
        -2: lambda deck: min(three_flip(deck)),
        -1: lambda deck: min(two_flip(deck)),
         0: lambda deck: one_flip(deck),
         1: lambda deck: max(two_flip(deck)),
         2: lambda deck: max(three_flip(deck)),
    }
    result = fns[mod](deck)
    return result > 2

def analyze(func, possible_results, *args):
    tries = 10000
    results = { x:0 for x in possible_results }
    for i in range(tries):
        results[func(*args)] += 1

    percents = [ pct(results[x], tries) for x in possible_results ]
    return (results, ' / '.join(percents))

def analyze_check(*args):
    return analyze(resolve_check, [True, False], *args)

def analyze_contest(*args):
    return analyze(resolve_contest, [-1, 0, 1], *args)

def analyze_contest_notie(*args):
    Notie.clear()
    analysis = analyze(Notie.resolve_contest, [-1, 1], *args)
    return analysis[0], analysis[1], Notie.analysis()



def proficiency_check(mod):
    c = cards[:]
    flips = abs(mod) + 1
    result = 0
    for i in range(flips):
        random.shuffle(c)
        card = c.pop()
        if card['Pro']:
            result += 1
    return result

def analyze_proficiency_check(mod):
    results = { x:0 for x in range(5) }
    for i in range(10000):
        results[proficiency_check(mod)] += 1
    return results

def p2_check(suit, mod):
    """
    Only take the 'Pro' if it's on the card that got used
    """
    if mod > 0:
        raise ValueError('die')

    c = cards[:]
    flips = abs(mod) + 1
    results = []
    for i in range(flips):
        random.shuffle(c)
        results.append(c.pop())

    score = 100
    used = None
    for card in results:
        if card[suit] < score:
            score = card[suit]
            used = card

    if used['Pro']:
        return 1
    return 0

def analyze_p2_check(*args):
    results = { x:0 for x in range(2) }
    for i in range(10000):
        results[p2_check(*args)] += 1
    return results

