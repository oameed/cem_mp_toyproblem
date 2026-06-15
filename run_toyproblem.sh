#! /bin/bash

source activate lnxpy

size=50000

python mp_toyproblem.py      -n $size

python mp_toyproblem_parl.py -n $size
