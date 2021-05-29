#! /bin/bash

set -e

if [ `basename $(pwd)` != "genesis" ]; then
  echo "You must be in the genesis directory to run this command"
  exit 1
fi

bin/build_components.sh

scp build/*png sjbrowngeeky@ezide.com:/home/sjbrowngeeky/ezide.com/GoDS/

bin/build_pdfs.sh

