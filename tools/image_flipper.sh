#!/bin/bash

for filename in *.png; do
	convert $filename -flop $filename
done
