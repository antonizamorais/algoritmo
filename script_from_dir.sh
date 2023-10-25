#!/bin/bash

# TODO: Write documentation.

# Check arguments and set variables
ARGC=$#
if [ $ARGC -ne 1 ]; then
    echo "Usage: $0 directory";
    exit;
fi
DIR=$1

for grammar in $DIR*.yrd; do
    [ -f "$grammar" ] || break
    grammar=$(realpath $grammar)
    for graph in $DIR*.txt; do
        [ -f "$graph" ] || break
        graph=$(realpath $graph)
        echo "$grammar,$graph,10"
    done
done
