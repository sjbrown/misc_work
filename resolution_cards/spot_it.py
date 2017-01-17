from itertools import *

def every_pair_has_one_match(deck):
    for card in deck:
        others = deck[:]
        others.remove(card)
        if not others:
            return True
        flattened_others = reduce(lambda x, y: x+y, others)
        accum = 0
        for symbol in card:
            accum += flattened_others.count(symbol)
        if accum != len(others):
            return False
    return True


def search(candidate_deck, remaining_choices, bad_pairs, finish_at):
    """
    Returns a list of decks that satisfy Spot-It rules
    """
    if not remaining_choices:
        return [candidate_deck]

    results = []
    if every_pair_has_one_match(candidate_deck):
        results.append(candidate_deck)

    for x in remaining_choices:
        if results and (len(results[-1]) == len(candidate_deck) + 1):
            # already found one of this length
            continue

        x_bad_pairs = set(combinations(x, 2))
        unseen_bad_pairs = x_bad_pairs.difference(bad_pairs)
        new_bad_pairs = bad_pairs.union(unseen_bad_pairs)

        if len(new_bad_pairs) == len(bad_pairs):
            new_space = remaining_choices
        else:
            new_space = reduce_search_space(
                remaining_choices,
                unseen_bad_pairs,
                candidate_deck,
            )

        new_decks = search(
            candidate_deck + [x],
            new_space,
            new_bad_pairs,
            finish_at,
        )
        new_decks = [
            x for x in new_decks
            if every_pair_has_one_match(x)
        ]

        if new_decks and len(new_decks[-1]) == finish_at:
            raise Exception(results + new_decks)

        results += new_decks

    return results

def reduce_search_space(orig_space, bad_pairs, orig_deck):
    return [
        card for card in orig_space
        if not(any(
            (a in card) and (b in card)
            for (a,b) in bad_pairs
        ))
    ]


def make_decks(num_symbols, symbols_per_card):
    all_choices = list(combinations(range(num_symbols), symbols_per_card))

    a = all_choices.pop(0)

    seed = [a]
    bad_pairs = set(combinations(a, 2))

    finish_at = (symbols_per_card - 1) + int(num_symbols**0.5)
    print 'finishing at length', finish_at

    return search(
        seed,
        reduce_search_space(all_choices, bad_pairs, seed),
        bad_pairs,
        finish_at,
    )
