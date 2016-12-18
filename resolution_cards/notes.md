# Premise / Guiding thoughts

It's fun to have decks of cards
 * It's fun to build a deck
 * It's fun to collect certain cards

Having rules on cards in front of you is better than having rules in a book
 * It takes more time to find the page with a particular rule

Arithmetic sucks.  Stop doing it.
 * "Flip 3, take the best" is way easier than roll 2d6, add your Strength bonus

Cards open up richer game play (unpredictable might be substituted for "random")
 * Dice:
  - carrying more than 10 is cumbersome
  - roll one to get a linear, bounded random value
  - roll multiple to get different distributions of random values
  - use a die as a marker
  - use a die & it's shown pip value as an enumerated marker
  - roll a die and hide its value for other players to guess
  - collect special dice
 * Cards:
  - carrying more than 200 is cumbersome
  - flip a card to get a bounded random value in whatever distribution the deck has
  - flip one to get multi-dimensional random values (eg, suit & number & face)
  - flip, without replacement, a series of cards from a deck with a ~known distribution
   - (deckbuilding mechanic)
  - flip a card and hide its value for other players to guess
  - collect special cards
   - collect cards that are normal in one dimension, but special in another
  - build a deck of cards (with dice this is possible, but cumbersome)
  - cards can be written on
  - cards can be drafted
  - player choice about when to shuffle can be interesting
  - the shuffle itself can be interesting
   - cut the deck
   - put a single card in the middle / at the bottom / on the top
   - look at top x cards, and put them back in any order
  - the backs can be
   - identical - to mask what the result will be
   - marked - to hint or make obvious what the result will be

----

# Character:

Trainable Attributes: (scores: red, yellow, green, blue)
 * Strength (muscles, endurance, constitution)
  * Dexterity (aim, catching, evasion)
   * Intelligence (charm, figuring, creation)
   Movement: Strength + Encumberance + Tiredness
   Personality: ??? Maybe the DM decides to throw in red or green cards based on personality
   Jason Bourne (4s in all categories) is possible, but throw in some other weakness / vulnerability to make the story good.

Common skills:
   Something that you have a clear idea how it works - climbing, ducking, lying, arguing, swimming
   To attempt:
    * Grab a blank card, write the skill on a card, put two red cards on top.  Decide which attribute governs it.  Flip 1 + (# of red cards).  Take lowest score.
     * If card has a proficiency symbol on it, discard one of the red cards.
      * etc
       * If you get a proficiency symbol when there are no red cards remaining, add a green card on top of the skill card.
        * From now on, flip 1 + (# of green cards) and take the highest score
         * Proficiency maxes out at 2 green cards

New skills:
 Something you've never seen anyone do before - new spell, duck call, snatch an arrow, swimming
 If you spend time watching carefully (no distractions) when someone succeeds in a skill, you can start it out with 4 red cards on top
 If someone spends time teaching you the basics, you can start it out with 3 red cards on top
 DM can choose to put a personality-block-card on a skill in critical or repeated failures

 New equipment they haven't used works the same way
  - except if they've used that "class" of equipment before, then they start with one red card (or one fewer green cards)
  - *except* if it's a clone.  One AK-47 is the same as any other.

> Note: this can mean that without a blessing, it is IMPOSSIBLE to get 2 green

Skills can be copied from D&D & Pathfinder
http://paizo.com/pathfinderRPG/prd/coreRulebook/feats.html

----
# Thematic flips:

  eg, a Chase / Running away
   * both characters can choose color direction up to their dexterity
   * runner gets a 1-card head start - looks at top card, decides which color to flip
   * runner flips up 2 green - chaser must exactly match the sum, so 3 green
   * chaser flips 1 green.  sum: 2 green
   * runner flips 1 green.  sum: 3 green
   * chaser flips 2 green. sum: 1 green
     some possibilities from here:
       - runner flips 1 red.  sum 0.  Runner is caught (runner hits dead end or trips)
       - runner flips 2 red. sum -1 (runner zigs the other way, still running.  chaser now needs 1 red)
   * if decks run out, runner has escaped
   * if runner gets a 5 point delta, runner has escaped

   - Chase doesn't have to be just for footraces.  Imagine if they're making a case to the town mayor, against the counter-arguments of an adversary.

### Silent Communication:
 * both characters silently pick up & look at the top card of their flip decks
 * they can then say exactly one word - the color they're going to flip (they can say it in any turn order, or DM can decide)
 * they then flip that color - if the points match, they succeed.


### Bluffing or deciding on gear could work like liar's dice
 - draw 5 of your cards, so does the opponent(s)
 - go around and say how many ✔s the whole group can make
 - eventually someone calls out the previous person
 - all cards are shown
 - if the callee has an attribute advantage, they can add that many extra cards (from the top of their deck)
 - but I have to make sure the distribution of ✗'s and ✔'s is even for that game.


### Blessing cards:
 * 2 green on all sides
 * color cards that go in the flip deck
 * awarded by the DM - maybe for roleplaying or for other epicness
 * they have 1 or 2 proficiency markers
 * once they come up & take their effect, they go back to the DM
   - similarly, lucky rings / amulets do the same thing, but when they come up they go under the character's ring/amulet card until appropriate to shuffle them back in

 Curse cards:
  * work similarly, awarded for similar reasons

### Combat:
      A series of X vs Y flips
      Landing blows can bruise, tire, wound, subdue, kill.

    Tire: (bruising can be the same but only for physical and you can't shake it off)
    - lvl 1: can't go to blue
    - lvl 2-4: get a red card
    - lvl 5: can't go to green
    - lvl 6: subdued

    Wound:
    - something becomes impossible, eg: broken arm - no sword swinging
    - bleeding - every time you get a red X, and every n minutes, you bruise
    - another wound and you're subdued


----

# Ok, better idea for Combat:

YY v YY - tie / clash
YY v Y   - deal a tiredness
YY v X   - deal a bruise
YY v XX - deal a wound

Y v Y - tie / clash - both parties take a tiredness
Y v X - deal a tiredness
Y v XX - deal a bruise

X v X - tie /clash - both parties take a bruise
X v XX - deal a tiredness

Must re-shuffle at 5 cards or lower

If you make a hit after opponent is fully tired (down to 10 cards),
If already wounded:
- they're subdued
If not:
- they flip a check for wounded or subdued

Wounds
bleeding - any time you make an action, flip one card and if it's marked for tiredness, discard it to the tired pile

----

# Ties

```
>>> analyze_contest_notie(d,d,2,2)
({-1: 4970, 1: 5030},
 '49.7% / 50.3%',
  "Ties 20527 (3.1x), {0: '32.6%', 1: '21.6%', 2: '15.2%', 3: '10.6%', 4: '6.8%', 5: '4.1%', 6: '2.9%', 7: '1.9%', 8: '1.6%', 9: '0.9%', 10: '0.5%', 11: '0.4%', 12: '0.3%', 13: '0.2%', 14: '0.1%', 15: '0.1%', 16: '0.1%', 17: '0.1%', 18: '0.0%', 20: '0.0%', 22: '0.0%'}")
```

What this says is that contests between decks where each player has a 2-proficiency bonus could
result in > 20 flips if the rule is "draw 3, take the best, on a tie, do it again".
Flipping 20 times is not going to be fun.

How to mitigate this?

 1. Ties are interpreted by the GM in a way that actually moves the narrative forward - no need to break them
 2. Players can get special "tie breaking" cards that narratively make sense
  * Character luck powers, etc
 3. Greatest count of ✔ marks on the cards (from the flipped suit) wins
  * Counting is annoying though.
  * If that's still tied, then the ✔ marks on all suits
   * If that's still tied, then the least ✗ marks
 4. Calculate the *difference* between proficiencies and flip based on that
  * Counting is annoying though.
  * That'll work for d+2 vs d+2 (calculate as d+0 vs d+0) , but does it give good results across suits? eg, d+2 vs c+1?
   * results: `d2/c2: 72/28`, `d0/c0: 60/40` `d2/c1: 82/18`, `d1/c0: 82/18`, `d2/b2: 78/22`, `d0/b0: 67/33`
   * Nope.

----

# Magic

Doing magic could work by actually performing a magic trick:
 * Declare what the next card is going to be:
 * flip purple side, "it's going to be double-check" - 8/20 chance
 * flip green side, "it's going to be single-check" - 6/20 chance
 * could motivate player to hold off on shuffling
 * therefore, it's advantageous for a caster to memorize stuff & understand the cards
 * BUT - does it make sense thematically in the *tired* deck?
  - sort of if you stipulate that they must guess number of checks


Doing magic could be:
 * Dominion-style deckbuilding
  - Maybe put bond & personality cards into the deck that affect performance
 * Set collection

----

# Armor

Maybe they have an armor card that where you can put "bruises" instead of
going to your body.  A couple examples:

 * A "standard armor" card: when taking a bruise, put it in one of 3 slots
   on this card, and take an "exhaustion" instead.
 * A "ethereal carapace" card: when taking a bruise, put it in one of 5 slots
   on this card.  Don't take an exhaustion.
 * A "shield" card: when taking a bruise, succeed a Dex check to put the bruise
   on this card, and take an "exhaustion" instead.

