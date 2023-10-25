INPUT=$1
OLDIFS=$IFS
IFS=','
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read grammar graph checksum repetitions gtype
do
    for ((i=0; i<$repetitions; i++))
    do
        echo "($i) $grammar $graph $checksum $repetitions $gtype"
        go run main.go $grammar $graph $checksum $gtype >> "$(dirname $INPUT)/result_$current_time.txt"
    done
done < $INPUT
IFS=$OLDIFS
