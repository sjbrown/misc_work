#! /bin/bash

set -e

if [ `basename $(pwd)` != "genesis" ]; then
  echo "You must be in the genesis directory to run this command"
  exit 1
fi

mkdir -p ./build
source bin/version.py

python2 bin/svg_dom.py pnp_songs1.svg
python2 bin/svg_dom.py pnp_songs2.svg
python2 bin/svg_dom.py pnp_band_first_song.svg
python2 bin/svg_dom.py pnp_character_sheet.svg
python2 bin/svg_dom.py pnp_chits.svg
python2 bin/svg_dom.py gig_board.svg
python2 bin/svg_dom.py lineup.svg
python2 bin/svg_dom.py downtime.svg
python2 bin/svg_dom.py band_meeting.svg
python2 bin/svg_dom.py crowd_track.svg

python2 bin/build_songs.py
python2 bin/build_png.py first_song_sheet.svg 2331 1906
python2 bin/build_png.py character_sheet.svg 2479 1063
python2 bin/build_png.py gig_board.svg 3508 2480
python2 bin/build_png.py downtime.svg 2480 3508
python2 bin/build_png.py band_meeting.svg 3508 2480
python2 bin/build_png.py crowd_track.svg 2480 3508

python2 bin/build_cards.py cards.svg
python2 bin/build_cards.py cards_gods.svg

python2 bin/build_cards.py song_part_chits.svg 250 250
cp /tmp/genesis$VERSION/card_rect_*chit*png ./build/

python2 bin/build_cards.py van_token.svg 250 250
cp /tmp/genesis$VERSION/card_rect_*van*png ./build/

python2 bin/build_cards.py encore_token.svg 250 250
cp /tmp/genesis$VERSION/card_rect_*encore*png ./build/

python2 bin/build_cards.py meep_tokens.svg 250 250
cp /tmp/genesis$VERSION/card_rect_*meep*png ./build/

#python2 bin/build_cards.py song_part_ovals_h.svg 250 250
#python2 bin/build_cards.py song_part_ovals_v.svg 250 250
#cp /tmp/genesis$VERSION/card_rect_oval*png ./build/

python2 bin/build_deck.py god
python2 bin/build_deck.py practice
python2 bin/build_deck.py gig
python2 bin/build_deck.py stress
#python2 bin/build_deck.py write_all
#python2 bin/build_deck.py write_beats
#python2 bin/build_deck.py write_melody
#python2 bin/build_deck.py write_front

for i in /tmp/genesis*; do
  echo $i
done

