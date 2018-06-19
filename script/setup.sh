#!/bin/bash

python make_vocab.py \
  --file data/01.mini.cdr \
  --vocab_file data/vocab \
  $*
