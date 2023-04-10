#!/bin/bash

ffmpeg \
     -r 4 \
     -f image2 \
     -s 1024x768 \
     -nostats \
     -loglevel 0 \
     -pattern_type glob \
     -i "*.jpg" \
     -vcodec libx264 \
     -crf 25 \
     -pix_fmt yuv420p \
     output.mp4
