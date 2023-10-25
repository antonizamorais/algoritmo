#!/bin/bash

# TODO: Write documentation.

# Check arguments and set variables
ARGC=$#
if [ $ARGC -ne 2 ]; then
    echo "Usage: $0 program experiments.csv";
    exit;
fi
PROGRAM=$1
CSV=$2

# Read csv and execute experiments
OLDIFS=$IFS
IFS=',' # Used to read the csv file
[ ! -f $CSV ] && { echo "$CSV file not found"; exit; }
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
newdir="exp_$current_time"
mkdir $newdir
while read grammar graph repetitions
do
    for ((i=0; i<$repetitions; i++))
    do
        echo "($i) $grammar $graph"
        ./$PROGRAM $grammar $graph ${@:3:99} >> "$newdir/result.txt"
    done
done < $CSV
IFS=$OLDIFS
