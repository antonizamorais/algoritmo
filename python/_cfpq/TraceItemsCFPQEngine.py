#!/usr/bin/env python3
from overrides import override

from graphs import Graph
from _cfpq.CFPQEngine import CFPQEngine
from provenance import Provenance


class TraceItemsCFPQEngine(CFPQEngine):
    '''The Trace-Items-based CFPQ evaluation engine.
    '''

    def __init__(self, *args, **kwargs):
        # Initialize common attributes in CFPQEngine
        super().__init__(*args, **kwargs)
        
        # Mapping of (vertex, symbol) pairs to their corresponding collections
        # of trace items
        # TODO: Rename self.R to self.I
        self.R = {}
        # List of position sets with new results to be processed
        self.NEW = []
        # Observer patter for position sets
        self.observers = {}


    def _get_or_create(self, a, X):
        '''Gets the collection of trace items for the pair (a,X).
        If the items do not exist, it creates them and properly updates `NEW`.
        '''
        if X not in self.G.nonterm:
            return None
        if (a, X) in self.R:
            return self.R[(a, X)]
        r = Relation(a, X)
        self.R[(a, X)] = r
        for rule in self.G.rules[X]:
            it = TraceItem()
            it.rule = [X] + rule
            it.posets = [PositionSet(set([a]))]
            it.posets[0].relation = r
            self.NEW.append((it, 0))
            for _ in rule:
                poset = PositionSet(set())
                poset.relation = r
                it.posets += [poset]
            r.items += [it]
        return r


    def _process_new(self, it, i):
        '''Processes all unprocessed vertices the position set at index `i` in
        trace item `it`.
        '''
        poset = it.posets[i]
        relation = poset.relation
        if i < len(it.rule)-1:
            # update next position set and NEW
            X = it.rule[i+1]
            next_poset = it.posets[i+1]
            new = set()
            destinations = None
            if X in self.G.term:
                requisitoOrigem = {}
                requisitoAresta = {}
                requisitoDestino = {}

                requisitoOrigem, requisitoAresta, requisitoDestino = Provenance.requisitos()
                propriedadesX = Provenance.propriedadesPROV(self.D, X, self.P)
                if requisitoOrigem in propriedadesX and requisitoAresta in propriedadesX and requisitoDestino in propriedadesX:
                    destinations = set()
                    for a in poset.new:
                        destinations.update(set(self.D.objects(a, X)))
            elif X in self.G.nonterm:
                destinations = set()
                for a in poset.new:
                    destinations.update(self._get_or_create(a, X).objects)
                    self.observers[(a, X)].add((it, i+1))
            if destinations is not None:
                new = False
                for b in destinations:
                    if b not in next_poset.nodes:
                        new = True
                        next_poset.new.add(b)
                if new:
                    self.NEW.append((it, i+1))
        else:
            # updates relation's objects and notifies observers
            new = set()
            for a in poset.new:
                if a not in relation.objects:
                    new.add(a)
            if len(new) > 0:
                relation.objects.update(new)
                for it2, j in self.observers[(relation.node, relation.symbol)]:
                    for n in new:
                        if n not in it2.posets[j].new:
                            it2.posets[j].new.add(n)
                            self.NEW.append((it2, j))
        poset.mark()

    @override
    def _pre_run(self):
        '''Initializes data structures.'''
        self.R = {} 
        self.NEW = []
        self.observers = {(a, s): set() for a in self.D.subj_data for s in self.G.nonterm}

    @override
    def _run(self):
        # Start algorithm
        for a, X in self.Q:
            self._get_or_create(a, X)

        while len(self.NEW) > 0:
            it, i = self.NEW.pop()
            if len(it.posets[i].new) > 0:
                self._process_new(it, i)

        result_count = 0
        for r in self.R.values():
            if r.symbol in self.G.nonterm:
                if (r.node, r.symbol) in self.Q:
                    result_count += len(r.objects)
        return result_count
    
    @override
    def _post_run(self):
        '''Produces the annotated graph D'.
        '''
        DPrime = Graph()
        for s, p, o, data in self.D:
            DPrime.add(s, p, o, data)
        for r in self.R.values():
            if r.symbol in self.G.nonterm:
                for o in r.objects:
                    DPrime.add(r.node, r.symbol, o)
        return DPrime


class Relation:
    '''A collection of trace items for a given (vertex, symbol) pair.
    It is useful to gather the answers for all trace items of the given pair.
    TODO: Find a better name.
    '''
    def __init__(self, node, symbol):
        self.node = node
        self.symbol = symbol
        self.objects = set()
        self.items = []

    def show(self):
        print('(', self.node, ',', self.symbol, ') =', self.objects)
        print('len(self.items) =', len(self.items))
        for it in self.items:
            it.show()
            print('')


class PositionSet:
    '''A position set for the trace-items-based algorithm.
    '''
    def __init__(self, new=set()):
        self.nodes = set()
        self.new = new
        self.relation = None
        self.data = {}

    def mark(self):
        '''Marks an entire position set as processed.
        `self.nodes` is updated with all vertices in `self.new` and `self.new`
        is emptied.
        '''
        self.nodes.update(self.new)
        self.new = set()
        return self.nodes

    def show(self):
        print('{', end=' ')
        for x in self.nodes:
            print(x, end=' ')
        for x in self.new:
            print(x+'*', end=' ')
        print('}', end='')

    def paint(self, vertex, color=0):
        '''Paints a vertex with a given color, represented by an integer.
        It is used by the context-free graph minimization algorithm.
        '''
        self.data.setdefault(vertex, {})['color'] = color

    def is_painted(self, vertex, color=0, ignore_absent=False):
        '''Checks whether a vertex is painted with a given or inferior color.
        It is used by the context-free graph minimization algorithm.
        '''
        d = None
        if ignore_absent:
            d = self.data.get(vertex, {})
        else:
            d = self.data[vertex]
        return d.get('color', -1) >= color


class TraceItem:
    '''A trace item for the trace-items-based algorithm.
    '''
    rule = []
    posets = []
    comparable = None

    def show(self):
        print(self.rule[0], '-> ', end=' ')
        self.posets[0].show()
        print(' ', end='')
        for i in range(1, len(self.rule)):
            print(self.rule[i], end=' ')
            self.posets[i].show()
            print(' ', end='')

    def symbol(self):
        return self.rule[0]

    def node(self):
        """
        Returns the only vertex in the first position set.
        """
        for x in self.posets[0].nodes:
            return x

    def __lt__(self, other):
        if self.comparable is None:
            self.comparable = ''.join(self.rule)
        if other.comparable is None:
            other.comparable = ''.join(other.rule)
        return (self.comparable < other.comparable)
