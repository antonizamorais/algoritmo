package main

import (
	"os"
	"rdf-ccfpq/go/ccfpq"
)

func main() {
	if len(os.Args) != 4 {
		panic("Usage: go run main.go grammar graph graphtype")
	}
	grammarfile := os.Args[1]
	graphfile := os.Args[2]
	graphtype := os.Args[3]
	G, D := ccfpq.QuickLoad(grammarfile, graphfile, graphtype)
	Q := ccfpq.QueryAll(G, D)
	ccfpq.RunExperiment(G, D, Q, -1)
}
