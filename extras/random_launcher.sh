#!/usr/bin/env bash

. ns-env/bin/activate

PYTHONPATH=/home/evan/neurosim/neural_style:$PYTHONPATH
python random_styler.py --input-dir /home/evan/images/inputs --output-dir /home/evan/images/outputs
