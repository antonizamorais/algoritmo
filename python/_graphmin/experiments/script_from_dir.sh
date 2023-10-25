dir=$1
[ -z "$dir" ] && echo "Usage: script_from_dir dir"

for graph in $dir*.txt; do
    [ -f "$graph" ] || break
    graph=$(realpath $graph)
		for grammar in $dir*.yrd; do
			[ -f "$grammar" ] || break
			grammar=$(realpath $grammar)
			for minimizer in "RandomRGM" "RandomCFGM"; do
			    echo "$minimizer,$grammar,$graph,10"
		done
	done
done
