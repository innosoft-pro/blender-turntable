#!/usr/bin/env bash

if [[ ! -z $2 ]]; then
    output="--turntable-output $2"
fi

blender turntable.blend --window-geometry 0 0 0 0 --python turntable.py -- --turntable-model $1 ${output}