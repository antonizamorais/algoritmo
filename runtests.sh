#!/bin/bash -

# Constants
EXP="experiments"
THEN=$( date +"%FT%H%M%S" )
RES="results/$THEN"
mkdir "$RES"
PUB="$RES/publish"
mkdir "$PUB"
ONT="$EXP/ontologies"
KJP="$EXP/kuijpers"
HGS="$EXP/hellings"
SYN="$EXP/synthetic"
GEO="$EXP/geospecies"
REP=10 # $1
HEADERS="test_result, grammarname, graphname, resultcount, time, memory"

echo "Running experiments..."
# Ontologies experiment
for grammar in "sc_t" "sc"
do
    for graph in "skos" "generations" "travel" "univ_bench" "foaf" "people_pets" "funding" "atom_primitive" "biomedical" "pizza" "wine" # "$ONT/"*".txt"
    do
        for ((i = 1; i <= REP; i++));
        do
            ./go/main "$ONT/$grammar.yrd" "$ONT/$graph.txt" >> "$RES/ontologies-$grammar-rep-$REP.tsv"
        done
    done
done


# Grigorev et al., Medeiros et al.
for grammar in "ab_ambiguous" "ab_unambiguous"
do
    for ((n = 0; n <= 500; n += 50));
    do
        for ((i = 1; i <= REP; i++));
        do
            ./go/main "$SYN/$grammar.yrd" "$SYN/complete-$n.txt" >> "$RES/complete-$grammar-rep-$REP.tsv"
        done
    done

    for ((n = 0; n <= 500; n += 50));
    do
        for ((i = 1; i <= REP; i++));
        do
            ./go/main "$SYN/$grammar.yrd" "$SYN/string-$n.txt" >> "$RES/string-$grammar-rep-$REP.tsv"
        done
    done
done


# Hellings
for grammar in "dense" "sparse"
do
    for ((n = 0; n <= 500; n += 50));
    do
        for ((i = 1; i <= REP; i++));
        do
            ./go/main "$HGS/$grammar.yrd" "$HGS/cycle-$n.txt" >> "$RES/cycle-$grammar-rep-$REP.tsv"
        done

        for ((i = 1; i <= REP; i++));
        do
            ./go/main "$HGS/$grammar.yrd" "$HGS/path-$n.txt" >> "$RES/path-$grammar-rep-$REP.tsv"
        done

        for ((i = 1; i <= REP; i++));
        do
            ./go/main "$HGS/$grammar.yrd" "$HGS/complete-$n.txt" >> "$RES/complete-$grammar-rep-$REP.tsv"
        done
    done
done


# Kuijpers
for k in 1 3 5 10
do
    for n in 100 500 2500 10000
    do
        for ((i = 1; i <= REP; i++));
        do
            ./go/main $KJP/an_bm_cm_dn.yrd "$KJP/abcd-n=$n-k=$k.txt" >> "$RES/kjp-figures23-rep-$REP.tsv"
        done
    done
done

n=500
for k in 1 3 5 10
do
    for ((i = 1; i <= REP; i++));
    do
        ./go/main $KJP/sparse.yrd "$KJP/abcd-n=$n-k=$k.txt" >> "$RES/kjp-table2-rep-$REP.tsv"
    done
done

n=100
k=5
for ((i = 1; i <= REP; i++));
do
    ./go/main $KJP/sl.yrd "$KJP/abcd-n=$n-k=$k.txt" >> "$RES/kjp-table3-rep-$REP.tsv"
done
for ((i = 1; i <= REP; i++));
do
    ./go/main $KJP/sr.yrd "$KJP/abcd-n=$n-k=$k.txt" >> "$RES/kjp-table3-rep-$REP.tsv"
done

n=100
k=5
for ((i = 1; i <= REP; i++));
do
    ./go/main $KJP/ambiguous.yrd "$KJP/abcd-n=$n-k=$k.txt" >> "$RES/kjp-table4-rep-$REP.tsv"
done

for ((i = 1; i <= REP; i++));
do
    ./go/main $GEO/bt.yrd "$GEO/geospecies9mb.txt" >> "$RES/kjp-table6-rep-$REP.tsv"
done
echo "Done"




./publish_results.sh $RES
