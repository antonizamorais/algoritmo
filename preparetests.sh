#!/bin/bash -

# Constants
EXP="experiments"
KJP="$EXP/kuijpers"
HGS="$EXP/hellings"
SYN="$EXP/synthetic"

# (re)build main binary
echo "Building main..."
rm -f go/main
go build -o go/main go/main.go
echo "Done"

echo "Generating synthetic data..."
# Hellings'
for ((n = 0; n <= 500; n += 50));
do
    python3 generators.py complete $n "A" > "$HGS/complete-$n.txt"
    python3 generators.py path $n "A" > "$HGS/path-$n.txt"
    python3 generators.py cycle $n "A" > "$HGS/cycle-$n.txt"
done

# Grigorev et al., Medeiros et al.
for ((n = 0; n <= 500; n += 50));
do
    python3 generators.py complete $n "A B" > "$SYN/complete-$n.txt"
    python3 generators.py string $n > "$SYN/string-$n.txt"
done

# Kuijpers'
for k in 1 3 5 10
do
    for n in 100 500 2500 10000
    do
        python3 generators.py kuijpers $n $k "A B C D" > "$KJP/abcd-n=$n-k=$k.txt"
    done
done

echo "Done"