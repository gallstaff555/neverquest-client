#!/bin/bash

# 'convert' command requires imagemagick installation:
# mac: brew install imagemagick
# debian: sudo apt-get install imagemagick

for filename in *.png; do
	convert $filename -flop $filename
done
