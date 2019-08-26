#!/usr/bin/env bash

if [ -f $4 ]; then
    exit 0
fi

export CUDA_VISIBLE_DEVICES=0
export NEURAL_STYLE_HOME=/home/evan/neurosim/neural-style

. ${NEURAL_STYLE_HOME}/ns-env/bin/activate
export PYTHONPATH=${NEURAL_STYLE_HOME}:$PYTHONPATH

python -u ${NEURAL_STYLE_HOME}/extras/specific_styler.py --content $1 --style $2 --scale $3 --output $4
