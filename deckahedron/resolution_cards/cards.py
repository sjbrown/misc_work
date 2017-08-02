#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from collections import defaultdict, OrderedDict

def pct(x, total):
    return '%04.1f%%' % (100*float(x)/total)

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
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 1, 'c': 3, 'd': 4},
 {'Pro': True , 'Tmark': True, 'a': 1, 'b': 2, 'c': 2, 'd': 4},
 {'Pro': True,  'Tmark': True, 'a': 3, 'b': 2, 'c': 1, 'd': 4},
 {'Pro': True,  'Tmark': True, 'a': 1, 'b': 4, 'c': 4, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 4, 'c': 3, 'd': 4},
 {'Pro': False, 'Tmark': True, 'a': 4, 'b': 3, 'c': 4, 'd': 2},
 {'Pro': False, 'Tmark': True, 'a': 3, 'b': 3, 'c': 1, 'd': 3},
]

def count_checks_in_suit(cards, suit):
    return sum(card[suit]-2 for card in cards if card[suit] >= 3)

def count_exes_in_suit(cards, suit):
    return sum(3-card[suit] for card in cards if card[suit] < 3)

blessing_cards = [
 {'Pro': False, 'Tmark': False, 'a': 4, 'b': 3, 'c': 4, 'd': 4, 'blessing': 'copper'},
 {'Pro': False, 'Tmark': False, 'a': 3, 'b': 4, 'c': 4, 'd': 4, 'blessing': 'copper'},
 {'Pro': False, 'Tmark': False, 'a': 4, 'b': 4, 'c': 4, 'd': 4, 'blessing': 'gold'},
 {'Pro': False, 'Tmark': False, 'a': 4, 'b': 4, 'c': 4, 'd': 4, 'blessing': 'gold'},
 {'Pro': False, 'Tmark': False, 'a': 4, 'b': 4, 'c': 4, 'd': 4, 'blessing': 'gold'},
 {'Pro': False, 'Tmark': False, 'a': 4, 'b': 4, 'c': 4, 'd': 4, 'blessing': 'gold'},
]

wound_cards = [
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 1, 'c': 1, 'd': 2, 'blessing': 'wound'},
 {'Pro': False, 'Tmark': False, 'a': 1, 'b': 1, 'c': 2, 'd': 1, 'blessing': 'wound'},
]

def flip(deck):
    # Takes a card off the deck and returns that new deck
    new_deck = deck[:]
    random.shuffle(new_deck)
    res = new_deck.pop()
    return res, new_deck

def flip_cards(cards, num=1):
    """
    Takes a card off the deck and returns that new deck

    Throws IndexError if there weren't eneough cards to flip
    """
    remaining = cards[:]
    random.shuffle(remaining)
    flipped = []
    for i in range(num):
        flipped.append(remaining.pop())
    return flipped, remaining

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


class TieReflip(object):
    """
    No ties allowed
    Just re-draw whenever there's a tie.

    This can be really shitty, because (d,d,2,2) or (a,a,-2,-2) can
    result in 1.7x the needed draws to get to a resolution.
    (see analyze_contest_tiereflip)
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

class TieCountChecks(object):
    """
    No ties allowed

    When a tie happens, try these:
     * most # of ✔s on the flipped suit on all flipped cards
     * most # of ✔s on all suits on all flipped cards
     * least # of ✗s on the flipped suit on all flipped cards
     * least # of ✗s on all suits on all flipped cards
     * flip again if none of that worked
    """
    ties = 0
    num_contests = 0
    tie_distribution = defaultdict(int)
    kind_distribution = defaultdict(int)

    @classmethod
    def resolve_contest_cards(cls,
        cards_a, suit_a, cards_b, suit_b, mod_a=0, mod_b=0,
        contest_ties=0
    ):
        if contest_ties == 0:
            cls.num_contests += 1
        howmany = {
            -3: 4,
            -2: 3,
            -1: 2,
             0: 1,
             1: 2,
             2: 3,
        }

        def tallys(flipped, mod, suit):
            if mod < 0:
                score_fn = min
            else:
                score_fn = max
            raw_score = score_fn(card[suit] for card in flipped)
            checks_in_suit = count_checks_in_suit(flipped, suit)
            checks_total = sum(count_checks_in_suit(flipped, s)
                               for s in ['a','b','c','d'])
            exes_in_suit = count_exes_in_suit(flipped, suit)
            exes_total = sum(count_exes_in_suit(flipped, s)
                               for s in ['a','b','c','d'])
            return [
                raw_score,
                checks_in_suit,
                checks_total,
                exes_in_suit,
                exes_total
            ]

        flipped_a, remaining_a = flip_cards(cards_a, howmany[mod_a])
        tally_a = tallys(flipped_a, mod_a, suit_a)
        flipped_b, remaining_b = flip_cards(cards_b, howmany[mod_b])
        tally_b = tallys(flipped_b, mod_b, suit_b)
        for i in range(len(tally_a)):
            result = cmp(tally_a[i], tally_b[i])
            if result != 0:
                if i > 0:
                    #print tally_a, tally_b
                    cls.kind_distribution[i] += 1
                cls.tie_distribution[contest_ties] += 1
                cls.ties += contest_ties
                return result
        return cls.resolve_contest_cards(
            remaining_a, suit_a,
            remaining_b, suit_b,
            mod_a, mod_b,
            contest_ties = contest_ties + 1
        )

    @classmethod
    def clear(cls):
        cls.ties = 0
        cls.num_contests = 0
        cls.tie_distribution = defaultdict(int)
        cls.kind_distribution = defaultdict(int)

    @classmethod
    def analysis(cls):
        mapp = {
                0: 'raw_score',
                1: 'chk in_suit',
                2: 'chk total',
                3: 'x in_suit',
                4: 'x total',
        }
        return 'Ties %s (%2.1fx) \n %s \n %s' % (
            cls.ties,
            cls.multiple(),
            {k:pct(v, cls.num_contests) for (k,v) in cls.tie_distribution.items()},
            {mapp[k]:v for (k,v) in cls.kind_distribution.items()},
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


def analyze_contest_tiereflip(*args):
    TieReflip.clear()
    analysis = analyze(TieReflip.resolve_contest, [-1, 1], *args)
    return analysis[0], analysis[1], TieReflip.analysis()

def analyze_contest_tiecountchecks(*args):
    TieCountChecks.clear()
    analysis = analyze(TieCountChecks.resolve_contest_cards, [-1, 1], *args)
    return analysis[0], analysis[1], TieCountChecks.analysis()


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


good_six_four_distributions = [
#00                   #         #
#01                   #         #        ##
#02         #         #        ##        ##         #         #         #
#03       ###         #        ##        ##        ##        ##        ##
#04     #####       ###        ##        ##     #####       ###      ####
#05       ###      ####        ##        ##      ####  ########     #####
#06       ###      ####        ##       ###       ###        ##      ####
#07        ##        ##      ####       ###       ###        ##        ##
#08        ##         #        ##        ##        ##         #        ##
#09         #         #        ##        ##                   #
#10                   #
 ([4, 0, 1, 1, 2, 4, 3, 2, 2, 0, 3, 4, 0, 0, 4, 1, 2, 3, 1, 3],
  [1, 4, 3, 6, 0, 2, 6, 1, 2, 5, 0, 2, 5, 6, 4, 3, 1, 5, 3, 4]),
 ([2, 1, 3, 4, 2, 3, 0, 1, 4, 1, 4, 3, 1, 0, 2, 4, 0, 0, 3, 2],
  [1, 5, 3, 4, 2, 6, 1, 6, 1, 3, 6, 3, 4, 4, 5, 2, 5, 0, 2, 0]),
 ([2, 1, 4, 1, 3, 0, 4, 0, 1, 4, 0, 2, 2, 0, 3, 3, 2, 1, 3, 4],
  [6, 4, 3, 6, 2, 2, 5, 1, 3, 2, 3, 4, 5, 0, 4, 0, 6, 1, 1, 5]),
 ([2, 2, 4, 1, 3, 0, 4, 0, 1, 4, 0, 4, 1, 3, 0, 2, 3, 1, 3, 2],
  [6, 4, 3, 6, 2, 2, 5, 5, 0, 2, 3, 4, 0, 3, 4, 5, 6, 1, 1, 1]),
 ([4, 0, 1, 1, 2, 4, 3, 2, 4, 0, 3, 2, 0, 0, 4, 1, 3, 2, 1, 3],
  [1, 4, 3, 6, 0, 4, 2, 1, 2, 5, 0, 6, 5, 6, 2, 3, 1, 5, 3, 4]),
 ([4, 0, 1, 1, 2, 2, 3, 2, 4, 0, 3, 2, 0, 0, 3, 1, 4, 4, 1, 3],
  [1, 4, 4, 6, 0, 3, 2, 1, 1, 5, 0, 6, 5, 6, 2, 3, 2, 5, 3, 4]),
 ([4, 2, 1, 1, 2, 4, 3, 2, 4, 0, 3, 2, 0, 0, 4, 1, 3, 0, 1, 3],
  [1, 4, 3, 6, 0, 4, 2, 1, 2, 5, 0, 6, 5, 6, 2, 3, 1, 5, 3, 4]),

#00                             #                   #
#01                            ##                   #        ##         #
#02       ###                  ##         #        ##        ##         #
#03       ###       ###        ##        ##        ##       ###        ##
#04       ###      ####        ##      ####       ###        ##       ###
#05       ###     #####        ##    ######        ##        ##     #####
#06        ##      ####        ##       ###        ##        ##       ###
#07        ##       ###         #        ##        ##        ##        ##
#08        ##         #        ##         #        ##        ##        ##
#09         #                  ##         #        ##        ##         #
#10         #                  ##                   #         #


 ([2, 2, 2, 1, 3, 0, 4, 0, 1, 4, 0, 1, 4, 3, 0, 3, 2, 1, 3, 4],
  [6, 4, 3, 6, 2, 2, 5, 3, 1, 2, 3, 4, 0, 0, 4, 5, 5, 1, 1, 6]), # this one is nice
 ([4, 1, 1, 1, 2, 4, 3, 2, 4, 0, 3, 2, 0, 0, 4, 1, 3, 2, 0, 3],
  [1, 4, 3, 6, 4, 0, 2, 1, 2, 5, 0, 6, 5, 6, 2, 3, 1, 5, 3, 4]),
 ([2, 4, 3, 4, 2, 3, 0, 1, 1, 4, 4, 2, 2, 0, 3, 1, 0, 0, 3, 1],
  [1, 5, 2, 4, 5, 6, 1, 2, 1, 6, 6, 3, 4, 4, 5, 0, 2, 0, 3, 3]),
 ([4, 1, 1, 1, 2, 4, 3, 2, 3, 0, 3, 2, 0, 0, 4, 1, 3, 2, 0, 4],
  [1, 6, 3, 4, 4, 0, 2, 1, 2, 5, 6, 0, 5, 6, 2, 3, 1, 5, 3, 4]), # this one is nice
 ([2, 4, 3, 4, 2, 0, 3, 1, 1, 4, 1, 2, 2, 0, 3, 1, 0, 0, 3, 4],
  [1, 5, 2, 4, 5, 6, 1, 3, 1, 6, 2, 3, 4, 4, 5, 0, 2, 0, 6, 3]),
 ([2, 2, 4, 1, 3, 0, 4, 0, 1, 3, 0, 4, 1, 3, 0, 2, 4, 1, 3, 2],
  [6, 1, 5, 6, 2, 2, 5, 3, 0, 2, 3, 4, 0, 3, 4, 5, 6, 1, 1, 4]),
 ([4, 2, 1, 1, 1, 4, 3, 2, 4, 0, 3, 2, 0, 0, 4, 2, 3, 0, 1, 3],
  [1, 4, 3, 6, 0, 4, 2, 1, 2, 5, 0, 6, 5, 6, 5, 3, 1, 2, 3, 4])
]

selected_six_four_distribution = 7

# I've distributed these such that the d4s are evenly split up
# among the exaustion / non-exaustion sets
dice_print_rules = [
 # 0 - d4:0
 ( (0, 2), 'six_sw_1 six_ne_1'
 ),
 # 1 - d4:1
 ( (1, 1), 'four_ne_1 six_sw_1'
 ),
 # 2 - d4:2
 ( (2, 6), 'four_sw_2 six_ne_2 six_nw_2 six_se_2'
 ),
 # 3 - d4:3
 ( (3, 5), 'four_sw_1 four_se_1 four_nw_1 six_ne_2 six_nw_1 six_sw_1 six_se_1'
 ),
 # 4 - d4:4
 ( (4, 0), 'four_nw_1 four_ne_1 four_se_1 four_sw_1'
 ),
 # 5 - d4:0
 ( (0, 3), 'six_sw_2 six_ne_1'
 ),
 # 6 - d4:1
 ( (1, 6), 'four_sw_1 six_ne_2 six_nw_2 six_se_2'
 ),
 # 7 - d4:2
 ( (2, 4), 'four_sw_1 four_ne_1 six_nw_2 six_se_2'
 ),
 # 8 - d4:3
 ( (3, 2), 'four_sw_2 four_ne_1 six_nw_1 six_se_1'
 ),
 # 9 - d4:4
 ( (4, 5), 'four_sw_2 four_se_1 four_nw_1 six_ne_2 six_nw_1 six_sw_1 six_se_1'
 ),
 # 10
 ( (4, 6), 'four_nw_1 four_ne_1 four_se_1 four_sw_1 six_sw_2 six_sw_1 six_ne_1 six_ne_2'
 ),
 # 11
 ( (3, 1), 'four_sw_2 four_ne_1 six_ne_1'
 ),
 # 12
 ( (2, 5), 'four_sw_2 six_ne_1 six_nw_2 six_se_2'
 ),
 # 13
 ( (1, 4), 'four_sw_1 six_ne_2 six_nw_1 six_se_1'
 ),
 # 14
 ( (0, 3), 'six_sw_2 six_ne_1'
 ),
 # 15
 ( (4, 2), 'four_nw_1 four_ne_1 four_se_1 four_sw_1 six_sw_1 six_ne_1'
 ),
 # 16
 ( (3, 0), 'four_sw_2 four_ne_1'
 ),
 # 17
 ( (2, 3), 'four_nw_1 four_se_1 six_sw_2 six_ne_1'
 ),
 # 18
 ( (1, 1), 'four_ne_1 six_sw_1 '
 ),
 # 19
 ( (0, 4), 'six_nw_1 six_ne_1 six_se_1 six_sw_1'
 ),
]

spot_it_rules = [
  (0, 1, 2, 3),
  (1, 9, 6, 4),
  (3, 5, 7, 6),
  (4, 0, 5, 8),
  (2, 7, 8, 9)
]
spot_it_map = {
  0: 'cow',
  1: 'horse',
  2: 'rabbit',
  3: 'rat',
  5: 'monkey',
  4: 'dog',
  6: 'tiger',
  7: 'snake',
  8: 'cock',
  9: 'pig',
}

def analyze_exes_and_checkmarks(svg=False, lost_stamina=0):
    a_deck = [x['a'] for x in cards]
    b_deck = [x['b'] for x in cards]
    c_deck = [x['c'] for x in cards]
    d_deck = [x['d'] for x in cards]
    all_decks = {
        'A': a_deck,
        'B': b_deck,
        'C': c_deck,
        'D': d_deck,
    }

    fns = {
        -3: lambda deck: min(four_flip(deck)),
        -2: lambda deck: min(three_flip(deck)),
        -1: lambda deck: min(two_flip(deck)),
         0: lambda deck: one_flip(deck),
         1: lambda deck: max(two_flip(deck)),
         2: lambda deck: max(three_flip(deck)),
    }
    results = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
    }
    possible_results = {
        1: u'✗✗',
        2: u'✗',
        3: u'✔',
        4: u'✔✔',
    }
    tries = 20000

    all_percents = []
    for rank, deck in all_decks.items():
        print ''
        print 'DECK ', rank
        print ''
        for mod in [-2, -1, 0, 1, 2]:
            mod_results = results.copy()
            for i in range(tries):
                deck_copy = deck[:]
                for x in range(lost_stamina):
                    # Remove one Stamina
                    deck_copy.pop( random.randint(10,len(deck_copy)-1) )
                fn = fns[mod]
                number = fn(deck_copy)
                mod_results[number] += 1

            if svg:
                group_id = '%s-mod%s' % (rank, mod)
                print '<g id="%s">' % group_id
                r = '''<rect style="fill:#{color};stroke:none;"
                    id="{rect_id}"
                    width="{width}"
                    height="4"
                    x="{x}"
                    y="{y}" />
                '''
                t = '''<text xml:space="preserve"
                   id="{text_id}"
                   x="{x}" y="{y}"
                   style="font-size:2px;
                       font-family:'Bebas Neue';
                       -inkscape-font-specification:'Bebas Neue';
                       fill:#000000
                       "
                   >
                   <tspan sodipodi:role="line" x="{x}" y="{y}" >{value}</tspan>
                </text>
                '''
                x = 0
                for j in [1,2,3,4]:
                    y = { 'A': 21, 'B': 14, 'C': 7, 'D': 0 }[rank]
                    color = {
                        1: 'd40000',
                        2: 'ff0000',
                        3: '55d400',
                        4: '44aa00',
                    }[j]
                    int_val = int(round((100*mod_results[j])/float(tries)))
                    print r.format(
                        rect_id=(group_id + '-' + str(j)),
                        width=int_val,
                        x=x,
                        y=y,
                        color=color,
                    )
                    if int_val > 0:
                        print t.format(
                            text_id=('text' + group_id + '-' + str(j)),
                            x=x*0.4,
                            y=y+5,
                            value=int_val
                        )
                    x += int_val
                print '</g>'

            else:
                print 'mod: ', mod
                print '✗✗', pct(mod_results[1], tries)
                print '✗ ',  pct(mod_results[2], tries)
                print '✔ ',  pct(mod_results[3], tries)
                print '✔✔', pct(mod_results[4], tries)

            percents = { x:pct(mod_results[x], tries) for x in mod_results.keys() }
            all_percents.append(percents)
    return all_percents

