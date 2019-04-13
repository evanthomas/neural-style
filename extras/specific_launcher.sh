#!/usr/bin/env bash

if [ -f $4 ]; then
    exit 0
fi

export CUDA_VISIBLE_DEVICES=0

BASE_DIR=/home/evan/neurosim/neural-style

. ${BASE_DIR}/ns-env/bin/activate

export PYTHONPATH=${BASE_DIR}:$PYTHONPATH
python -u ${BASE_DIR}/extras/specific_styler.py --content $1 --style $2 --scale $3 --output $4
