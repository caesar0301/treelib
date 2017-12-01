#!/usr/bin/env bash

nosetests --with-coverage --cover-package=treelib \
    --cover-erase --cover-tests \
    -d --all-modules \
    tests
