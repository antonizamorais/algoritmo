import sys, math, os

def latex_table(filenames):
    tabbegin = '''

\\begin{table}[htpb]
\\centering
\\begin{tabular}{@{}llrrrr@{}}
\\toprule
\\textbf{Grammar} & \\textbf{Graph} & \\textbf{$|V|$} & \\textbf{Results} & \\textbf{Time} & \\textbf{Memory} \\\\'''
    tabend = '''\\bottomrule
\\end{tabular}
\\caption{'''+str([os.path.basename(f) for f in filenames]).replace('_','\_')+'''}
\\label{tab:my-table}
\\end{table}'''
    print(tabbegin)
    for filename in filenames:
        print('\\midrule\n')
        output = _avg_values(_as_dict(filename))
        for out in output:
            print(out['grammar'], '&', out['graph'], '&', out['vertices'], '&', out['results'], '&', '%d ms'%(out['time']), '&', '%.1f Mb'%(out['memory']),'\\\\')
    print(tabend)

def _as_dict(filename):
    data = {}
    lines = open(filename,'r').readlines()
    for l in lines:
        values = l.split('\t')
        G = values[1] #.replace('_','\\_')
        D = values[2].replace('_','\\_')

        G = G[G.rfind('/')+1:] if '/' in G else G
        G = G[:G.rfind('.yrd')] if '.yrd' in G else G
        G = '$G_{\\ref{gram:' + G + '}}$'

        D = D[D.rfind('/')+1:-4]
        D = D[:D.rfind('.txt')] if '.txt' in D else D

        vertices = int(values[3])
        edges = int(values[4])
        results = int(values[5])
        time = int(values[6])
        memory = float(values[7])
        data.setdefault(G,{}).setdefault(D,{})
        data[G][D].setdefault('vertices',[]).append(vertices)
        data[G][D].setdefault('edges',[]).append(edges)
        data[G][D].setdefault('results',[]).append(results)
        data[G][D].setdefault('time',[]).append(time)
        data[G][D].setdefault('memory',[]).append(memory)
    return data

def _avg_values(data):
    out = []
    for G in data:
        for D in data[G]:
            vertices = data[G][D]['vertices'][0]
            results = data[G][D]['results'][0]
            avg = {}
            for v in data[G][D]:
                avg[v] = sum(data[G][D][v]) / len(data[G][D][v])
            out += [{
                'grammar' : G,
                'graph' : D,
                'vertices' : vertices,
                'results' : results,
                'time' : avg['time'],
                'memory' : avg['memory'],
            }]
    return out

def latex_chart(filenames):
    chartbegin = '''

\\begin{tikzpicture}
    \\begin{axis}[
        height=5cm,
        width=7cm,
        grid=major,
        legend pos=north west,
        xlabel=vertices,
        ylabel=%s
    ]
'''
    chartend = '''\\end{axis}
\\end{tikzpicture}'''

    for ylabel, y in [('Time (ms)', 'time'), ('Memory (MB)', 'memory')]:
        print(chartbegin%(ylabel))
        for filename in filenames:
            print('\\addplot coordinates {',end='')
            output = _avg_values(_as_dict(filename))
            for out in output:
                print(' (%d, %d)'%(out['vertices'],out[y]), end='')
            print('};')
            print('\\addlegendentry{',os.path.basename(filename).replace('_','\_'),'};')
        print(chartend)

if __name__ == '__main__':
    assert len(sys.argv) >= 2, "Usage: "+sys.argv[0]+" <format> <path/to/file1.tsv> <path/to/file2.tsv> ..."

    formats = list(filter(callable,locals().values()))
    fmtname = sys.argv[1]
    fmt = None
    for f in formats:
        if fmtname == f.__name__:
            fmt = f
            break
    if not fmt:
        print('Bad format name. Available formats: ',end='')
        for name in [f.__name__ for f in formats]:
            if not name.startswith('_'):
                print(name, end=' ')
        print()
        exit(1)
    fmt(sys.argv[2:])
