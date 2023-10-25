'''
Graphs and related data structures for path query algorithms.
'''

class Graph:
    '''A Graph data structure for path query algorithms.
    Use the `load` method to read data from a file.
    '''

    def __init__(self, name=''):
        self.subj_data = {}
        self.obj_data = {}
        self.triples_count = 0
        self.name = name

    def __len__(self):
        '''Allows the use of the `len` function to get the amount of triples
        in the graph.'''
        return self.triples_count

    def __iter__(self):
        '''Makes the Graph iterable.'''
        for s, sindex in self.subj_data.items():
            for p, pindex in sindex.edges.items():
                for o, data in pindex.items():
                    yield (s, p, o, data)

    def add(self, subj, pred, obj, data=None):
        '''Adds a triple.
        '''
        self.subj_data.setdefault(subj, Node(subj))
        self.subj_data.setdefault(pred, Node(pred))
        self.subj_data.setdefault(obj, Node(obj))

        self.obj_data.setdefault(subj, Node(subj))
        self.obj_data.setdefault(pred, Node(pred))
        self.obj_data.setdefault(obj, Node(obj))

        self.subj_data[subj].edges.setdefault(pred, {})
        self.obj_data[obj].edges.setdefault(pred, {})

        oins = obj not in self.subj_data[subj].edges[pred]
        sino = subj not in self.obj_data[obj].edges[pred]
        assert oins == sino, 'Inconsistency in graph'

        if obj not in self.subj_data[subj].edges[pred]:
            self.triples_count += 1
        self.subj_data[subj].edges[pred][obj] = data
        self.obj_data[obj].edges[pred][subj] = data

    def remove(self, subj, pred, obj):
        '''Removes a triple.
        '''
        del self.subj_data[subj].edges[pred][obj]
        if len(self.subj_data[subj].edges[pred]) == 0:
            del self.subj_data[subj].edges[pred]
            if len(self.subj_data[subj].edges) == 0:
                del self.subj_data[subj]
        del self.obj_data[obj].edges[pred][subj]
        if len(self.obj_data[obj].edges[pred]) == 0:
            del self.obj_data[obj].edges[pred]
            if len(self.obj_data[obj].edges) == 0:
                del self.obj_data[obj]
        self.triples_count -= 1

    def update(self, subj, pred, obj, data):
        '''Updates the data of a triple.
        '''
        self.subj_data[subj].edges[pred][obj] = data
        self.obj_data[obj].edges[pred][subj] = data

    def subjects(self, pred, obj):
        '''Returns the subjects for all triples matching the pattern 
        `(?subject, pred, obj)`.
        '''
        for s in self.obj_data[obj].edges.get(pred, set()):
            yield s

    def predicate_objects(self, subj):
        '''Returns the predicates and objects for all triples matching the
        pattern `(subj, ?predicate, ?object)`.
        '''
        for pred in self.subj_data[subj].edges:
            for dest in self.subj_data[subj].edges[pred]:
                yield (pred, dest)

    def predicates(self, subj, obj=None):
        '''Returns the predicates for all triples matching the pattern 
        `(subj, ?predicate, obj)`.
        TODO: Fix this. The function is returning objects, not predicates.
        '''
        for pred in self.subj_data[subj].edges:
            return self.objects(subj, pred)

    def subject_objects(self, pred):
        '''Returns the subjects and objects for all triples matching the pattern 
        `(subject, ?pred, object)`.
        '''
        for s, sindex in self.subj_data.items():
            for o in sindex.get(pred, []):
                yield (s, o)

    def objects(self, subj, pred):
        '''Returns the objects for all triples matching the pattern 
        `(subj, pred, ?object)`.
        '''
        for o in self.subj_data[subj].edges.get(pred, {}):
            yield o

    def all_subjects(self):
        '''Returns all triples' subjects.'''
        for s in self.subj_data:
            if len(self.subj_data[s].edges) > 0:
                yield s

    def all_nodes(self):
        '''Return all triples' subjects and/or objects.
        '''
        for subj in self.subj_data:
            yield subj
            for pred in self.subj_data[subj].edges:
                for obj in self.subj_data[subj].edges[pred]:
                    yield obj

    def weight(self, subj, pred, obj):
        '''Returns the weight of a triple.
        '''
        return self.subj_data[subj].edges[pred][obj]['weight']

    def total_weight(self):
        '''Returns the sum of all triple weights.
        '''
        # TODO: make total an attribute to avoid computing it
        total = 0.0
        for _, _, _, data in self:
            total += data['weight']
        return total

    def paint_edge(self, s, p, o, color=1):
        '''Paints a vertex with given color, represented by an integer.
        '''
        self.subj_data[s].edges[p][o]['color'] = color

    def edge_is_painted(self, s, p, o, color=-1):
        """
        Checks whether an edge is painted. Returns `True` if the color of an
        edge is >= `color`. In case one needs to clean colors of edges, e.g.
        during a search, instead of cleaning the whole graph, they need only to
        pick a new color greater than all old ones (usually incrementing it by
        1).
        """
        if 'color' not in self.subj_data[s].edges[p][o]:
            return False
        return self.subj_data[s].edges[p][o]['color'] >= color

    def paint_vertex(self, x, color=1):
        '''Paints a vertex with given color, represented by an integer.
        '''
        self.subj_data[x].data['color'] = color
        self.obj_data[x].data['color'] = color

    def vertex_is_painted(self, x, color=-1):
        """
        Checks whether a vertex is painted. Returns `True` if the color of a
        vertex is >= `color`. In case one needs to clean colors of vertices, e.g.
        during a search, instead of cleaning the whole graph, they need only to
        pick a new color greater than all old ones (usually incrementing it by
        1).
        """
        if 'color' not in self.subj_data[x].data:
            return False
        return self.subj_data[x].data['color'] >= color

    def show(self):
        '''Prints all triples and data.
        '''
        for s, p, o, data in self:
            print(s, p, o, data)

    def data(self, s, p, o):
        '''Returns data associated with a triple.
        '''
        return self.subj_data[s].edges[p][o]

    def __contains__(self, triple):
        '''Allows the use Python's `in` operator.
        '''
        s, p, o = triple
        if s in self.subj_data:
            if p in self.subj_data[s].edges:
                if o in self.subj_data[s].edges[p]:
                    return True
        return False

    @staticmethod
    def load(graphfile, headers=None, grammar=None):
        """
        Loads a Graph from a graph file.
        If lines in the data file have more than 3 values, i.e., edges contain
        data, `headers` must be a list of pairs (key, type) for assigning edge
        data as data[key] = type(f).
        If `grammar` is not None, restricts edges to its alphabet.
        """
        D = Graph()
        D.name = graphfile
        for line in _read_graph_file(graphfile):
            s, p, o, *fields = line
            mustadd = p in grammar.term if grammar is not None else True
            if mustadd:
                data = {}
                for i, f in enumerate(fields):
                    key, _type = headers[i]
                    data[key] = _type(f)
                D.add(s, p, o, data)
        return D


class Node:
    '''A node or vertex.
    Contains a local index of outgoing edges.
    Supports assigning data to it.
    '''
    def __init__(self, label):
        self.label = label
        self.edges = {}
        self.data = {}


def _read_graph_file(graphfile):
    # TODO: delete this function
    """
    Reads tuples in a graph file.
    """
    f = open(graphfile, 'r')
    for line in f.readlines():
        if line:
            yield line.strip('\n').split(' ')
    f.close()
