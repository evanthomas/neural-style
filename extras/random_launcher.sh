#!/usr/bin/env bash

export NEURAL_STYLE_HOME=/home/evan/neurosim/neural-style

. $NEURAL_STYLE_HOME/ns-env/bin/activate

export PYTHONPATH=$NEURAL_STYLE_HOME:$PYTHONPATH
python -u random_styler.py --input-dir /data/images/inputs-2048 --output-dir /home/evan/neurosim/images/outputs
