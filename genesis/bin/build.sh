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
python2 bin/build_cards.py song_part_ovals_h.svg 250 250
python2 bin/build_cards.py song_part_ovals_v.svg 250 250
python2 bin/build_bandpractice_songs.py new_song.svg
python2 bin/build_deck.py god
python2 bin/build_deck.py practice
python2 bin/build_deck.py gig
python2 bin/build_deck.py spite
python2 bin/build_deck.py write
python2 bin/build_deck.py write_beats
python2 bin/build_deck.py write_melody
python2 bin/build_deck.py write_front

for i in /tmp/genesis*; do
  echo $i
done

source bin/version.py

sed -e "s/VERSION/$VERSION/" rules.md > /tmp/rules.md

# To handle emoji --latex-engine=xelatex is necessary
pandoc --latex-engine=xelatex -V 'mainfont:DejaVu Sans' /tmp/rules.md -o /tmp/genesis_rules.pdf

# since pdftk is installed via snap, it can't access /tmp.
rm -f $HOME/tmp/genesis*.pdf
mv /tmp/genesis*.pdf $HOME/tmp/

if `which pdftk`; then
  pdftk $HOME/tmp/genesis*.pdf cat output $HOME/tmp/genesis_print_and_play.pdf
else
  pdfjoin --rotateoversize=false $HOME/tmp/genesis*.pdf --outfile $HOME/tmp/genesis_print_and_play.pdf
fi

echo "DONE. Find finished PDF here:"
echo ""
echo "$HOME/tmp/genesis_print_and_play.pdf"
echo ""


