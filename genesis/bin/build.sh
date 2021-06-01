#! /bin/bash

set -e

if [ `basename $(pwd)` != "genesis" ]; then
  echo "You must be in the genesis directory to run this command"
  exit 1
fi

source bin/version.py
UNIQUE=$(head -5c /dev/urandom | base32)


if [ -d /tmp/genesis$VERSION ]; then
  mv /tmp/genesis$VERSION /tmp/genesis$UNIQUE
fi

if [ -d ./build ]; then
  mv ./build /tmp/genesis_build$UNIQUE
fi

mkdir /tmp/genesis$VERSION
mkdir -p ./build

bin/build_components.sh

scp ./build/*png sjbrowngeeky@ezide.com:/home/sjbrowngeeky/ezide.com/GoDS/$VERSION/

bin/build_pdfs.sh

