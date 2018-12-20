#!/bin/bash

SOURCE=source
PYLIB=../treelib
TARGET=html
BUILT=build

rm -rf $BUILD
sphinx-apidoc -o $SOURCE $PYLIB
make $TARGET
touch $BUILT/$TARGET/.nojekyll
ghp-import -p $BUILT/$TARGET
