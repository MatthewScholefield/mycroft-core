#!/bin/bash

# Place this script and map.txt into a folder
# with wav files named 01.wav to 27.wav and run
# to rename to appropriate name assuming they were
# recorded by changing the intensity, then changing
# the distance, and lastly changing the background noise
# starting from low and increasing to high

initials=${PWD##*/}
initials=$(echo $initials | tr '[:upper:]' '[:lower:]')

while read -r old new; do
    mv "$old.wav" "$new.$initials.wav"
done < map.txt
