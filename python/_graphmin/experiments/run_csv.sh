INPUT=$1
PYSCRIPT=$2
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
[ ! -f $PYSCRIPT ] && { echo "$PYMOD file not found"; exit 99; }

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
res="exp_$current_time.txt"
echo "agorithm  grammar graph |V| |E| old weight	new weight	approx. ratio time path query time graph min	memory path query  memory graph min" >> "$res"
while read minimizer grammar graph optimum repetitions
do
    for ((i=0; i<$repetitions; i++))
    do
        echo "($i) $minimizer $grammar $graph"
        python3 $PYSCRIPT $minimizer $grammar $graph $optimum ${@:3:99} >> "$res"
    done
done < $INPUT
IFS=$OLDIFS
