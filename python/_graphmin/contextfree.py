import collections

from behaviors import RandomicBehavior
from cfpq import TraceItemsCFPQEngine
from graphs import Graph
from util import get_time, get_memory


class RandomCFGM:
    """
    Randomic context-free-language-constrained graph minimizer.
    """

    def minimize(self, graph, grammar, query, behavior=RandomicBehavior):
        self._iter = behavior.iter
        ti_engine = TraceItemsCFPQEngine(grammar, graph, query)
        nres, DPrime, timecfpq, memcfpq = ti_engine.run()
        DMin, timegmin, memgmin = self._minimize(DPrime, grammar, query, ti_engine.R)
        cfpqstats = {'results': nres, 'time': timecfpq, 'mem': memcfpq}
        gminstats = {'time': timegmin, 'mem': memgmin}
        return DMin, {'pq': cfpqstats, 'gmin': gminstats}

    def _minimize(self, DPrime, G, Q, R):
        DMin = Graph()
        answers = {}
        t0 = get_time()
        m0 = get_memory()
        color = 1
        for a, X in self._iter(Q):
            for b in self._iter(R[(a, X)].objects):
                if (a, X, b) not in answers:
                    for item in self._iter(R[(a, X)].items):
                        if b in item.posets[-1].nodes:
                            edges = self.path_edges(b, DMin, DPrime, G, R,
                                                    item, len(item.posets)-1,
                                                    answers, color)
                            if edges is not None:
                                if (a, X, b) not in answers:
                                    answers[(a, X, b)] = edges
                                break
                self.answer(a, X, b, DMin, DPrime, G, answers)
                color += 1
        t1 = get_time()
        m1 = get_memory()
        return DMin, t1-t0, m1-m0

    def path_edges(self, b, DMin, DPrime, G, R, item, i, answers, color):
        X = item.rule[i]
        if i == 0:
            empty = set()
            if len(item.rule) == 1:
                answers[(b, X, b)] = empty  # loop edge
            return empty
        elif i == len(item.posets)-1:
            if item.posets[i].is_painted(b, color=color, ignore_absent=True):
                res = answers.get((item.node(), item.symbol(), b), None)
                return res
            else:
                item.posets[i].paint(b, color=color)
        subjects = collections.deque()
        for a in self._iter(item.posets[i-1].nodes):
            if a in DPrime.subjects(X, b):
                if (a, X, b) in DMin:  # Try to reuse added edges first
                    subjects.appendleft(a)
                else:
                    subjects.append(a)
        for a in subjects:
            edges = None
            if X in G.term:
                edges = {(a, X, b)}
            elif X in G.nonterm:
                for item2 in self._iter(R[(a, X)].items):
                    last = len(item2.rule)-1
                    if b in item2.posets[last].nodes:
                        if self.path_edges(b, DMin, DPrime, G, R, item2, last,
                                           answers, color) is not None:
                            edges = {(a, X, b)}
                            break
            else:
                raise ValueError("%s must be a symbol." % (X))
            if edges is not None:
                edges2 = set()
                if i > 1:
                    edges2 = self.path_edges(a, DMin, DPrime, G, R, item, i-1,
                                             answers, color)
                if edges2 is not None:
                    edges.update(edges2)
                    if (item.node(), X, b) not in answers:
                        answers[(item.node(), X, b)] = edges
                    return edges

    def answer(self, a, X, b, DMin, DPrime, G, answers):
        for (s, p, o) in answers[(a, X, b)]:
            if p in G.term:
                DMin.add(s, p, o, DPrime.data(s, p, o))
            elif p in G.nonterm:
                self.answer(s, p, o, DMin, DPrime, G, answers)
            else:
                raise ValueError("%s must be a symbol." % (p))
