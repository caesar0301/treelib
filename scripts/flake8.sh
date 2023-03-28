#!/bin/bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-line-length=127 --exclude docs/source/conf.py --statistics
