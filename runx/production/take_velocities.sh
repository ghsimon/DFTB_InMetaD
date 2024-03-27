#!/bin/bash

INPUT=../random_equilibration/geo_end.xyz
FILE=velocities.dat
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else
    tail -n 26 $INPUT | awk '{print $6" "$7" "$8 }' | tail -n +1  > $FILE
fi
