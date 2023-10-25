import collections

from graphs import Graph
from _graphmin.automata import ProductAutomaton, Automaton
from behaviors import RandomicBehavior
from util import get_time, get_memory


def _dfs_paths(a, q1, color, prodauto, DMin, iter_f):
    """
    Returns the set of edges for each path from `(a, q1)` to all reachable
    final states by performing depth-first search.
    `color` is an integer used to paint vertices.
    """
    prodauto.paint_vertex((a, q1), color)
    if (a, q1) in prodauto.final_states:
        yield set(), a
    # TODO: avoid recomputing paths from an already processed (a, q1)
    aux = (((a, q1), p, (b, q2)) for p, (b, q2) in
           prodauto.iter(prodauto.predicate_objects((a, q1))))
    for _, p, (b, q2) in _painted_first(aux, DMin, iter_f):
        if prodauto.vertex_is_painted((b, q2), color):
            continue
        prodauto.paint_vertex((b, q2), color)
        edge = (a, p, b)
        path = set()
        if (b, q2) in prodauto.final_states:
            path.add(edge)
            mustclean = (yield path, b)
            if mustclean is not None:
                if mustclean:
                    path = set()
        for path, last_b in _dfs_paths(b, q2, color, prodauto, DMin, iter_f):
            path.add(edge)
            yield path, last_b


def _bfs_paths(v0, q0, color, prodauto, DMin):
    """
    Returns the set of edges for each path from `(v0, q0)` to all reachable
    final states by performing breadth-first search.
    `color` is an integer used to paint vertices.
    """
    class Transition:
        def __init__(self, v, q, p, parent):
            self.vertex = v
            self.state = q
            self.pred = p
            self.parent = parent
    root = Transition(v0, q0, None, None)
    queue = collections.deque()
    queue.append(root)
    prodauto.paint_vertex((v0, q0), color)
    while len(queue) > 0:
        t = queue.popleft()
        v1, q1 = t.vertex, t.state
        # build path to yield
        if (v1, q1) in prodauto.final_states:
            par = t.parent
            curr = t
            b = t.vertex
            path = set()
            while par is not None:
                p = curr.pred
                edge = (par.vertex, p, curr.vertex)
                path.add(edge)
                curr = par
                par = par.parent
            yield path, b
        # continue on breadth-first seach
        aux = [((v1, q1), p2, (v2, q2)) for p2, (v2, q2) in
               prodauto.iter(prodauto.predicate_objects((v1, q1)))]
        for _, p2, (v2, q2) in _painted_first(aux, DMin):
            if not prodauto.vertex_is_painted((v2, q2), color):
                queue.append(Transition(v2, q2, p2, t))
                prodauto.paint_vertex((v2, q2), color)


def _painted_first(edges, DMin, iter_f):
    """Iterates over painted edges first."""
    sortededges = collections.deque()
    for (a, q1), p, (b, q2) in iter_f(edges):
        if (a, p, b) in DMin:
            sortededges.appendleft(((a, q1), p, (b, q2)))
        else:
            sortededges.append(((a, q1), p, (b, q2)))
    return sortededges


class RandomRGM:
    """
    Random regular-language-constrained graph minimizer.
    """

    def minimize(self, graph, grammar, query, behavior=RandomicBehavior,
                 search_f=_dfs_paths, **kwargs):
        t0 = get_time()
        m0 = get_memory()
        prodauto = ProductAutomaton(
            graph,
            Automaton(name=grammar, grammar=grammar),
            behavior=behavior)
        rpqstats = {'time': get_time() - t0, 'mem': get_memory() - m0}
        t0 = get_time()
        m0 = get_memory()
        DMin, _, _ = self._minimize(prodauto, graph, query, behavior.iter, search_f)
        gminstats = {'time': get_time() - t0, 'mem': get_memory() - m0}
        return DMin, {'pq': rpqstats, 'gmin': gminstats}

    def _minimize(self, prodauto, graph, query, iter_f, search_f):
        DMin = Graph()
        color = 0
        answers = set()
        for a, q in iter_f(query):
            color += 1
            path_gen = search_f(a, q, color, prodauto, DMin, iter_f)
            hasnext = True
            # To avoid adding repeated edges in case we find an overlapping
            # path, we pass mustclean=True to path_gen.send. This discards
            # the path just added.
            # To initialize a generator with send, however, we must pass None.
            mustclean = None
            while hasnext:
                try:
                    path, b = path_gen.send(mustclean)
                    mustclean = False
                    if (a, b) not in answers:
                        mustclean = True
                        answers.add((a, b))
                        for s, p, o in path:
                            data = graph.data(s, p, o)
                            DMin.add(s, p, o, data)
                except StopIteration:
                    hasnext = False
        return DMin, answers, color
