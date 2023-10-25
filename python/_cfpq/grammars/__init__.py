# TODO: Move this module to the python source code root directory
class Grammar:
    def __init__(self):
        self.name = ''
        self.rules = {}
        self.term = set()
        self.nonterm = set()
        self.start_symbol = None
        self.nullable = set()

    def show(self):
        print('Start symbol:', self.start_symbol)
        print('Term:', self.term)
        print('Non-term:', self.nonterm)
        print('Nullable:', self.nullable)
        for lhs in self.rules:
            for rhs in self.rules[lhs]:
                print(lhs, '->', rhs)

    @staticmethod
    def load(path):
        f = open(path, 'r')
        g = Grammar()
        g.name = path
        rules = []
        for line in f.readlines():
            line = line.strip(' \n')
            rules += [line.split(' ')]
        g.start_symbol = rules[0][0]  # must set start symbol before sorting rules
        rules.sort(key=len)
        for rule in rules:
            lhs = rule[0]
            rhs = rule[1:]
            if lhs not in g.rules:
                g.rules[lhs] = []
            g.rules[lhs] += [rhs]
            if len(rhs) == 0:
                g.nullable.add(lhs)
            g.term.update(rhs)      # non-terminals will be removed next
        f.close()
        for lhs in g.rules:
            if lhs in g.term:
                g.term.remove(lhs)  # remove non-terminals
            g.nonterm.add(lhs)
        return g
