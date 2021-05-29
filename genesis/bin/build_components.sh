#! /bin/bash

set -e

if [ `basename $(pwd)` != "genesis" ]; then
  echo "You must be in the genesis directory to run this command"
  exit 1
fi

python2 bin/svg_dom.py src.svg
python2 bin/build_cards.py cards.svg
python2 bin/build_cards.py cards_gods.svg
python2 bin/build_cards.py song_part_chits.svg 250 250
python2 bin/build_cards.py meep_tokens.svg 250 250
python2 bin/build_cards.py song_part_ovals_h.svg 250 250
python2 bin/build_cards.py song_part_ovals_v.svg 250 250
python2 bin/build_bandpractice_songs.py new_song.svg
python2 bin/build_deck.py god
python2 bin/build_deck.py practice
python2 bin/build_deck.py gig
python2 bin/build_deck.py stress
python2 bin/build_deck.py write_all
python2 bin/build_deck.py write_beats
python2 bin/build_deck.py write_melody
python2 bin/build_deck.py write_front

for i in /tmp/genesis*; do
  echo $i
done

source bin/version.py

mkdir build
mv /tmp/genesis$VERSION/build_deck_* build/
