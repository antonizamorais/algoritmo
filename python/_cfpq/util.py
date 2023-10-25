""" Useful functions """

# TODO: Move contents to python/util.py
def load_grammar(g):  # Used by LL-based CFPQ evaluation engine
    grammar = None
    if 'synthetic/ab_ambiguous' in g:
        from _cfpq.grammars.ab_ambiguous import grammar
    elif 'synthetic/ab_unambiguous' in g:
        from _cfpq.grammars.ab_unambiguous import grammar
    elif 'ontologies/sc_t.yrd' in g:
        from _cfpq.grammars.sc_t import grammar
    elif 'ontologies/sc.yrd' in g:
        from _cfpq.grammars.sc import grammar
    elif 'ontologies/sc_t_cnf.yrd' in g:
        from _cfpq.grammars.sc_t_cnf import grammar
    elif 'ontologies/sc_cnf.yrd' in g:
        from _cfpq.grammars.sc_cnf import grammar
    elif g == 'bt':
        from _cfpq.grammars.bt import grammar
    elif 'hellings/dense' in g:
        from _cfpq.grammars.hlg_dense import grammar
    elif 'hellings/sparse' in g:
        from _cfpq.grammars.hlg_sparse import grammar
    elif 'kuijpers/anbmcmdn' in g:
        from _cfpq.grammars.kjp_an_bm_cm_dn import grammar
    elif g == 'kjp_ambiguous':
        from _cfpq.grammars.kjp_ambiguous import grammar
    elif g == 'kjp_dense':
        from _cfpq.grammars.kjp_dense import grammar
    elif g == 'kjp_sparse':
        from _cfpq.grammars.kjp_sparse import grammar
    elif g == 'kjp_sl':
        from _cfpq.grammars.kjp_sl import grammar
    elif g == 'kjp_sr':
        from _cfpq.grammars.kjp_sr import grammar
    else:
        assert False, 'Bad grammar name: '+g
    return grammar
