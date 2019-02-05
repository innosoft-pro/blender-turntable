#!/usr/bin/env bash

for file in models/*.dae
do
    ./turntable.sh "$file" render/$(basename ${file}) 1
    ffmpeg -i "render/$(basename ${file})/distance 0 height 0/%04d.png" -vf scale=640:360 render/$(basename ${file}).gif
done