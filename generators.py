'''Python script for generating synthetic graphs.'''
import random, sys, os, re

'''Auxiliary functions'''
def _counter():
    c = 0
    while True:
        c += 1
        yield c

'''Generator functions'''
def complete(n, labels='A B'):
    """ Generates a complete with n nodes. """
    n = int(n)
    predicates = labels.split(' ')
    graph = []
    for i in range(1,n+1):
        s = str(i)
        for p in predicates:
            for j in range(1,n+1):
                o = str(j)
                graph += [[s,p,o]]
    _to_file(graph)
    return graph

def path(n, labels='A'):
    """ Generates a path graph with n+1 nodes. """
    n = int(n)
    predicates = labels.split(' ')
    graph = []
    for i in range(1,n):
        s = str(i)
        for p in predicates:
            o = str(i+1)
            graph += [[s,p,o]]
    _to_file(graph)
    return graph

def string(n):
    """ Generates a string graph with n+1 nodes.
    The first half is labeled with A's and the second one with B's."""
    n = int(n)
    graph = []
    half = int(n/2)
    p = "A"
    for i in range(1,half+1):
        s = str(i)
        o = str(i+1)
        graph += [[s,p,o]]
    p = "B"
    for i in range(half+1,n):
        s = str(i)
        o = str(i+1)
        graph += [[s,p,o]]
    _to_file(graph)
    return graph

def cycle(n, labels='A'):
    """ Generates a cycle graph with n nodes. """
    n = int(n)
    if n<=0: return
    predicates = labels.split(' ')
    graph = path(n, labels)
    remainder = []
    s = str(n)
    o = "1"
    for p in predicates:
        remainder += [[s,p,o]]
    graph += remainder
    _to_file(remainder)
    return graph

def kuijpers(n,k,labels='A B C D'):
    n = int(n)
    k = int(k)
    L = labels.split(' ')
    assert n >= k, 'It is required that n >= k'

    def label(L):
        return random.choice(L)

    def add(D,i,j,I,var):
        l = label(L)
        D += [[i,l,j]]
        D += [[j,l+"R",i]]
        if i == len(I):
            I += [0]
        I[j] += 1
        I[i] += 1
        var['sum'] += 2

    def p(i,I,sumI):
        if sumI == 0:
            return 1
        return (I[i]) / sumI

    D = [] # the graph
    I = [] # vertices' degree
    var = {'sum' : 0} # sum of vertices' degree
    for i in range(k):
        for j in range(k):
            if i != j:
                l = label(L)
                D += [[i,l,j]]
                D += [[j,l+"R",i]]
    I = [(k-1)*2]*k
    var['sum'] = (k-1)*2*k
    for i in range(k,n):
        chosenset = set()
        chosensum = 0.0
        for _ in range(k):
            r = random.uniform(0,1-chosensum)
            for j in range(len(I)):
                pj = p(j,I,var['sum'])
                if j not in chosenset:
                    if r <= pj:
                        break
                    r -= pj
            chosenset.add(j)
            chosensum += p(j,I,var['sum'])
        for j in chosenset:
            add(D,i,j,I,var)

    _to_file(D)
    return D

def mutations(n, h, m=2, l=4, choices='ABCD'):
    def next_i(seq):
        return index_counter.__next__() % len(seq)
    def new_mutation(parent, child, index, fr, to, seq):
        mut = 'm' + str(mut_counter.__next__())
        return [
            [parent, 'mutation', mut],
            [mut, '^mutation', parent],
            [mut, 'index', index],
            [index, 'self::'+index, index],
            [mut, 'from', fr],
            [fr, 'self::'+fr, fr],
            [mut, 'to', to],
            [to, 'self::'+to, to],
            [mut, 'result', child],
            [child, '^result', mut]
        ]
    def mutation_tree(parent, seq, n, h, cap):
        if n == 1 or h == 1:
            return []
        n -= 1
        cap -= 1
        graph = []
        j = 0
        while n > 0 and j < m:
            child = parent+'.'+str(j+1)
            i = next_i(seq)
            index = str(i+1)
            fr = seq[i]
            to = random.sample(choices-set(fr), 1)[0]
            graph += new_mutation(parent, child, index, fr, to, seq)
            hj = h - 1
            capj = (m**hj) - 1
            maxnj = min(capj, n)
            minnj = 1
            if n > (cap - capj):
                minnj = n - (cap - capj)
            if re.fullmatch('1(\.1)*', child):
                minnj = max(minnj, hj)
                assert minnj <= n, 'minnj > n = %d > %d' % (minnj, n)
            if j == m-1:
                minnj = maxnj
            assert minnj <= maxnj, 'n=%d cap=%d hj=%d capj=%d minnj=%d maxnj=%d' % (n, cap, hj, capj, minnj, maxnj)
            nj = random.randint(minnj, maxnj)
            n -= nj
            cap -= nj
            graph += mutation_tree(child, seq[:i]+to+seq[i+1:], nj, hj, capj)
            j += 1
        assert n == 0, '%d != 0' % (n)
        return graph
    choices = set(choices)
    mut_counter = _counter()
    index_counter = _counter()
    n = int(n)
    h = int(h)
    m = int(m)
    l = int(l)
    cap = (m**h)-1
    assert m <= len(choices), 'm > len(%s)' % (choices)
    assert n <= cap, "Cannot add %d vertices to a tree of height %d and arity %d" % (n, h, m)
    assert n >= h, "Cannot reach height %d with %d vertices" % (h, n)
    sys.setrecursionlimit(h+15)
    _to_file(mutation_tree('1','A'*(l), n, h, cap))
    assert mut_counter.__next__() == n

def _to_file(D):
    for s,p,o in D:
        print(str(s)+" "+str(p)+" "+str(o))

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print('Usage: python',os.path.basename(__file__),'<generator> [<args...>]')
        exit(1)

    generators = list(filter(callable,locals().values()))
    gen_name = args[0]
    gen = None
    for g in generators:
        if gen_name == g.__name__:
            gen = g
            break
    if not gen:
        print('Bad generator name. Available generators: ',end='')
        for name in [g.__name__ for g in generators]:
            if not name.startswith('_'):
                print(name, end=' ')
        print()
        exit(1)
    gen(*tuple(args[1:]))
