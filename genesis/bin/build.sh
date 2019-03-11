#! /bin/bash

set -e

if [ `basename $(pwd)` != "genesis" ]; then
  echo "You must be in the genesis directory to run this command"
  exit 1
fi

python bin/svg_dom.py src.svg

for i in /tmp/genesis*; do
  echo $i
done

# To handle emoji --latex-engine=xelatex is necessary
pandoc --latex-engine=xelatex rules.md -o /tmp/genesis_rules.pdf

# since pdftk is installed via snap, it can't access /tmp.
rm $HOME/tmp/genesis*.pdf
mv /tmp/genesis*.pdf $HOME/tmp/

pdftk $HOME/tmp/genesis*.pdf cat output $HOME/tmp/genesis_print_and_play.pdf

echo "DONE. Find finished PDF here:"
echo ""
echo "$HOME/tmp/genesis_print_and_play.pdf"
echo ""


