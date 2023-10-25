package ccfpq

import (
	"fmt"
	"io/ioutil"
	"os"
	ds "rdf-ccfpq/go/data_structures"
	"rdf-ccfpq/go/util"
	"runtime"
	"strings"
	"time"
)

type (
	NodeSet struct {
		nodes    ds.VertexSet
		new      ds.VertexSet
		prev     *Symbol
		next     *Symbol
		relation Relation
	}

	pair struct {
		node   ds.Vertex
		symbol ds.Vertex
	}
)

var (
	R   relationsSet
	NEW []*NodeSet
	O   observersSet
)

/* NodeSet Methods and Functions */
func NewNodeSet() *NodeSet {
	return &NodeSet{
		nodes: f.NewVertexSet(),
		new:   f.NewVertexSet(),
	}
}

func (ns *NodeSet) Mark() {
	for k := range ns.new.Iterate() {
		ns.nodes.Add(k)
	}
	ns.new = f.NewVertexSet()
}

func GetOrCreate(node, label ds.Vertex, G *Grammar) Relation {
	r := R.get(node, label)
	if r == nil {
		if label.Equals(epsilon()) {
			panic("Should not create empty relations")
		} else if G.NestedExp.Contains(label) {
			r2 := NewNestedRelation(node, label)
			// G.Rules[label][0][0] gets symbol S from rule [S] -> S
			r2.SetRule([]ds.Vertex{G.Rules[label][0][0]})
			r = r2
		} else if G.NonTerm.Contains(label) {
			r2 := NewNonTerminalRelation(node, label)
			startVertices := f.NewVertexSet()
			startVertices.Add(node)
			for _, rule := range G.Rules[label] {
				r2.AddRule(startVertices, rule, G)
			}
			r = r2
		} else if G.Alphabet.Contains(label) {
			// do nothing (do not delete this if clause)
		} else {
			panic("Should not create expression relations")
		}
		if r != nil {
			R.set(node, label, r) // do not add nil relations
		}
	}
	return r
}

/* pair Methods and Functions */
func newPair(node, symbol ds.Vertex) *pair {
	return &pair{
		node:   node,
		symbol: symbol,
	}
}

/* Graph Parsing Functions */
func BuildBaseGraph(graph ds.Graph, grammar *Grammar) ds.Graph {
	D := f.NewGraph(graph.Name())
	D.SetName(graph.Name())
	for pElem := range grammar.Alphabet.Iterate() {
		p := pElem.(ds.Vertex)
		for pair := range graph.SubjectObjects(p) {
			s := pair[0]
			o := pair[1]
			D.Add(s, p, o)
		}
	}
	return D
}

func AddNew(nodeSet *NodeSet) {
	NEW = append(NEW, nodeSet)
}

func processNew(nodeSet *NodeSet, G *Grammar) {
	if symbol := nodeSet.next; symbol != nil {
		// update symbol's object set and NEW
		new := f.NewVertexSet()
		for a := range nodeSet.new.Iterate() {
			var destinations ds.VertexSet = f.NewVertexSet()
			if symbol.predicate.Equals(epsilon()) {
				destinations.Add(a)
			} else {
				if r := GetOrCreate(a, symbol.predicate, G); r != nil {
					destinations = r.Objects()
				}
				if !G.Alphabet.Contains(symbol.predicate) {
					O.add(a, symbol.predicate, symbol.objNodeSet)
				}
			}
			for b := range destinations.Iterate() {
				if !symbol.objNodeSet.nodes.Contains(b) {
					new.Add(b)
				}
			}
		}
		if new.Size() > 0 {
			symbol.objNodeSet.new.Update(new)
			AddNew(symbol.objNodeSet)
		}
	} else {
		// updates relation's objects and notifies O
		new := f.NewVertexSet()
		if nodeSet.relation.IsNested() && nodeSet.relation.Objects().Size() == 0 {
			new.Add(nodeSet.relation.Node())
		} else {
			for a := range nodeSet.new.Iterate() {
				if !nodeSet.relation.Objects().Contains(a) {
					new.Add(a)
				}
			}
		}
		if new.Size() > 0 {
			nodeSet.relation.AddObjects(new)
			for _, o := range O.get(nodeSet.relation.Node(),
				nodeSet.relation.Label()) {
				for n := range new.Iterate() {
					if !o.new.Contains(n) {
						o.new.Add(n)
						AddNew(o)
					}
				}
			}
		}
	}
	nodeSet.Mark()
}

func pickAndRemove() *NodeSet {
	i := len(NEW) - 1
	ns := NEW[i]
	NEW[i] = nil
	NEW = NEW[:i]
	return ns
}

func Run(D ds.Graph, G *Grammar, Q []pair) (relationsSet, time.Duration, uint64) {
	os.Setenv("GOGC", "off")
	// allocateMemory(15000)
	runtime.GC()
	// var startmem runtime.MemStats
	// runtime.ReadMemStats(&startmem)

	startusr, startsys := util.GetTime()

	R = f.NewRelationsSet()
	O = f.NewObserversSet()

	// Creating terminal relations
	for s := range D.AllSubjects() {
		for p := range D.Predicates(s) {
			objects := f.NewVertexSet()
			ds.ChanToSet(D.Objects(s, p), objects)
			R.set(s, p, NewTerminalRelation(s, p, objects))
		}
	}

	// Initializing non-terminal relations
	for _, p := range Q {
		var r *NonTerminalRelation
		var node ds.Vertex
		label := p.symbol
		var startVertices ds.VertexSet

		if super, isSuperVertex := p.node.(ds.SuperVertex); isSuperVertex {
			node = super.Vertex
			startVertices = super.Vertices
		} else {
			node = p.node
			startVertices = f.NewVertexSet()
			startVertices.Add(node)
		}
		r = NewNonTerminalRelation(node, label)
		for _, rule := range G.Rules[label] {
			r.AddRule(startVertices, rule, G)
		}
		R.set(node, label, r)
	}

	for len(NEW) > 0 {
		if n := pickAndRemove(); n != nil {
			processNew(n, G)
		}
	}

	endusr, endsys := util.GetTime()
	usrtime := time.Duration(endusr - startusr)
	systime := time.Duration(endsys - startsys)

	runtime.GC()
	var endmem runtime.MemStats
	runtime.ReadMemStats(&endmem)
	memory := endmem.Alloc
	os.Setenv("GOGC", "100")
	return R, usrtime + systime, memory
}

func QuickLoad(grammarfile string, graphfile string, factoryType string) (*Grammar, ds.Graph) {
	graph, grammar := LoadInfo(grammarfile, graphfile)
	VAlloc := graph.VSize()
	EAlloc := grammar.Alphabet.Size() + grammar.NonTerm.Size() +
		grammar.NestedExp.Size() + 1
	SetFactory(factoryType, VAlloc, EAlloc)
	D := f.NewGraph(graph.Name())
	for triple := range graph.Iterate() {
		s := f.NewVertex(triple[0].Label())
		p := f.NewPredicate(triple[1].Label())
		o := f.NewVertex(triple[2].Label())
		D.Add(s, p, o)
	}
	var G *Grammar
	switch factoryType {
	case SLICE_FACTORY:
		G = NewGrammar()
		G.Name = grammar.Name
		G.StartSymbol = f.NewPredicate(grammar.StartSymbol.Label())
		for s := range grammar.Alphabet.Iterate() {
			G.Alphabet.Add(f.NewPredicate(s.Label()))
		}
		for s := range grammar.NonTerm.Iterate() {
			G.NonTerm.Add(f.NewPredicate(s.Label()))
		}
		for e := range grammar.NestedExp.Iterate() {
			G.NestedExp.Add(f.NewPredicate(e.Label()))
		}
		for lhs, rules := range grammar.Rules {
			lhsbit := f.NewPredicate(lhs.Label())
			for _, rhs := range rules {
				var rhsbit []ds.Vertex
				for i := range rhs {
					rhsbit = append(rhsbit, f.NewPredicate(rhs[i].Label()))
				}
				G.AddRule(lhsbit, rhsbit)
			}
		}
	case SIMPLE_FACTORY:
		G = grammar
	default:
		panic(fmt.Sprint("Unknown factory type ", factoryType))
	}
	return G, D
}

func LoadInfo(grammarfile string, graphfile string) (ds.Graph, *Grammar) {
	f = NewSimpleFactory()
	grammar := LoadGrammar(grammarfile)
	data, err := ioutil.ReadFile(graphfile)
	if err != nil {
		panic("Error openning file: " + graphfile + "\n")
	}
	lines := strings.Split(string(data), "\n")
	graph := f.NewGraph(util.GetFileName(graphfile)).(*ds.SimpleGraph)
	for _, line := range lines {
		if line != "" {
			triple := strings.Split(line, " ")
			if len(triple) != 3 {
				fmt.Println("Error reading line:\n", line)
				return nil, nil
			}
			p := f.NewPredicate(triple[1])
			if grammar.Alphabet.Contains(p) {
				graph.LoadTriple(triple)
			}
		}
	}
	return graph, grammar
}
