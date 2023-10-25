from util import get_memory, get_time

class CFPQEngine:
    '''Base CFPQ engine class.
    Other CFPQ engines must inherit from this class and implement the `_run` 
    method.
    Optionally, they can also implement the `_pre_run` and `_post_run` methods
    to add pre- and pos-query instructions.
    '''
    def __init__(self, grammar, graph, provenance, query):
        self.G = grammar
        self.D = graph
        self.Q = query
        self.P = provenance


    def run(self):
        '''Template method for running a CFPQ evaluation algorithm.'''
        # Run pre-query instructions
        self._pre_run()
        
        # Get memory and time before algorithm starts
        m0 = get_memory()
        t0 = get_time()
        
        # Run the algorithm
        number_of_answers = self._run() 

        # Get memory and time after algorithm finishes and calculate resource
        # usage
        t1 = get_time()
        m1 = get_memory()
        time = t1 - t0
        memory = m1 - m0

        # Run post-query instructions
        DPrime = self._post_run()

        return number_of_answers, DPrime, time, memory


    def _pre_run(self):
        '''Runs before a query.
        Useful for allocating resources, for example.
        '''
        pass
    

    def _run(self):
        '''Abstract method to be impemented by concrete CFPQEngine subclasses.
        Runs the query.'''
        raise Exception('Abstract method. Must be implemented by CFPQEngine subclasses.')
    

    def _post_run(self):
        '''Runs after a query.
        Useful for releasing resources or processing the output, for example.
        '''
        pass
    

    def run_experiment(self, **kwargs):
        '''Runs a query and prints performance data.
        '''
        result_count, DPrime, time, memory = self.run()
        exp_data = [
            ('engine', type(self).__name__),
            ('grammar', self.G.name),
            ('graph', self.D.name),
            ('provenance', self.P.name)
            ('results', result_count),
            ('time', time),
            ('memory', memory)
        ]
        self._print_experiment_data(exp_data, **kwargs)


    @staticmethod
    def _print_experiment_data(experiment_data, print_headers=False):
        if print_headers:
            for header, _ in experiment_data:
                print(header, end='\t')
            print() # New line
        for _, data in experiment_data:
            print(data, end='\t')
        print() # New line
