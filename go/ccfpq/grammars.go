package ccfpq

import (
	"fmt"
	"io/ioutil"
	ds "rdf-ccfpq/go/data_structures"
	"rdf-ccfpq/go/util"
	"strings"
)

const OPEN = "["
const CLOSE = "]"

type Grammar struct {
	Name        string
	Rules       map[ds.Vertex][][]ds.Vertex
	Alphabet    ds.VertexSet
	NonTerm     ds.VertexSet
	NestedExp   ds.VertexSet
	StartSymbol ds.Vertex
}

func NewGrammar() *Grammar {
	return &Grammar{
		NonTerm:     f.NewVertexSet(),
		Alphabet:    f.NewVertexSet(),
		NestedExp:   f.NewVertexSet(),
		Rules:       make(map[ds.Vertex][][]ds.Vertex),
		StartSymbol: nil, // mimicking a zero value for the StartSymbol
	}
}

func (g *Grammar) AddNonTerminals(nonterminals ds.VertexSet) {
	for n := range nonterminals.Iterate() {
		g.NonTerm.Add(n)
	}
}

func (g *Grammar) AddNestedExpressions(exps ds.VertexSet) {
	for e := range exps.Iterate() {
		g.AddNestedExpression(e)
	}
}

func (g *Grammar) AddNestedExpression(exp ds.Vertex) {
	g.NestedExp.Add(exp)
}

func (g *Grammar) AddRule(lhs ds.Vertex, rhs []ds.Vertex) {
	g.Rules[lhs] = append(g.Rules[lhs], rhs)
	if !g.NestedExp.Contains(lhs) {
		g.NonTerm.Add(lhs)
	}
	g.Alphabet.Remove(lhs)
	for _, s := range rhs {
		if g.NonTerm.Contains(s) || s.Equals(epsilon()) {
			// do nothing
		} else if g.NestedExp.Contains(s) {
			// do nothing
		} else {
			g.Alphabet.Add(s)
		}
	}
}

func (g *Grammar) Show() {
	fmt.Print("N = ")
	g.NonTerm.Show()
	fmt.Print("\nT = ")
	g.Alphabet.Show()
	fmt.Print("\nNE = ")
	g.NestedExp.Show()
	fmt.Println()

	for lhs := range g.Rules {
		for _, rhs := range g.Rules[lhs] {
			fmt.Println(lhs, "->", rhs)
		}
	}
}

func LoadGrammar(path string) *Grammar {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		panic("Error openning file: " + path + "\n")
	}
	lines := strings.Split(string(data), "\n")
	g := NewGrammar()
	g.Name = util.GetFileName(path)
	for _, line := range lines {
		rule := parseExp(line)
		if len(rule) > 0 {
			lhs := rule[0]
			if g.StartSymbol == nil {
				g.StartSymbol = lhs
			}
			rhs := []ds.Vertex{f.NewPredicate("")}
			if len(rule) > 1 {
				rhs = rule[1:]
			}
			for _, s := range rhs {
				if isNestedExp(s) {
					g.AddNestedExpression(s)
					inner := f.NewPredicate(strings.Trim(s.Label(), "[]"))
					g.AddRule(s, []ds.Vertex{inner})
				}
			}
			g.AddRule(lhs, rhs)
		}
	}
	return g
}

func parseExp(exp string) []ds.Vertex {
	rule := []ds.Vertex{}
	if exp != "" {
		for _, str := range strings.Split(exp, " ") {
			rule = append(rule, f.NewPredicate(str))
		}
	}
	return rule
}

func isNestedExp(exp ds.Vertex) bool {
	nested := false
	if _, ok := exp.(ds.BitVertex); ok {
		panic("Not implemented yet.")
	} else if str, ok := exp.(ds.SimpleVertex); ok {
		nested = strings.HasPrefix(str.Label(), OPEN) &&
			strings.HasSuffix(str.Label(), CLOSE)
	} else {
		panic("Unknown vertex type.")
	}
	return nested
}

func epsilon() ds.Vertex {
	return f.NewPredicate("")
}
