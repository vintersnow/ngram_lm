#!/bin/sh

rsync -a --progress \
  --exclude __pycache__\
  --exclude data \
  --exclude .git \
  --exclude *.log \
  --exclude logs \
  --exclude *.pickle \
  --exclude venv-pypy \
  -e ssh ~/Projects/ut/nlp/slp_work/n-gram kobe:~/projects/
