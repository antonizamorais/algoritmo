LANG=$1
RES=$2
PUB=$3

echo "Publishing results in Latex format..."
echo "" > $PUB/latex.tex
python3 formatresults.py latex_table "$RES/$LANG-ontologies-sc_t-rep-"*".tsv" "$RES/$LANG-ontologies-sc-rep-"*".tsv" "$RES/$LANG-kjp-table6-rep-"*".tsv" >> "$PUB/latex.tex"

for graph in string complete
do
    python3 formatresults.py latex_chart "$RES/$LANG-$graph-ab_ambiguous-rep-"*".tsv" "$RES/$LANG-$graph-ab_unambiguous-rep-"*".tsv" >> "$PUB/latex.tex"
done

for graph in cycle path complete
do
    python3 formatresults.py latex_chart "$RES/$LANG-$graph-hlg_dense-rep-"*".tsv" "$RES/$LANG-$graph-hlg_sparse-rep-"*".tsv" >> "$PUB/latex.tex"
done

for f in "$RES/$LANG-kjp-"*".tsv"
do
    python3 formatresults.py latex_table $f >> "$PUB/latex.tex"
done
echo "Done"
