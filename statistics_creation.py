import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import time
import igraph as ig
import pickle
from math import log


class transaction:
    
    def __init__(self, piece):
        tx = piece.split('\n#\n')      
        self.Hash = tx[0]
        self.date = tx[1]
        self.input_keys = tx[2].split('\n')
        self.output_keys = tx[3].split('\n')
        self.BTC = tx[4].split('\n')
        
    def loop(self):
        return set(self.input_keys) == set(self.output_keys)

    def __str__(self):
        return (
            self.Hash + self.date + str(self.input_keys) 
            + str(self.output_keys) + str(self.BTC)
        )


def get_number(BTC):
    return float(BTC[:-3].replace(',', ''))

#graph statistics

folder = ''
for filename in [
    '07', '09', '10', '11', '12', '13', 
    '24', '25', '26', '27', '28', '29', '30'
    ]:
    G = ig.Graph.Read_Pickle(folder + filename + ' aug graph.txt')
    fout = open(filename + ' aug stats.txt', 'w')
    value = ' BTC '
    cut_vertices = G.cut_vertices()
    cutvertices = len(cut_vertices)
    weak_components = len(G.clusters(mode='WEAK'))
    stats = str()
    stats += str(G.vcount()) + ' nodes, ' + str(G.ecount()) + ' edges,'
    tx_number = str(len(open(
        'transactions/' 
        + filename 
        + ' aug transactions full correct.txt', 
        encoding='cp1251').read().split('\n\n\n')))
    stats += tx_number + ' bitcoin transactions\n'
    
    
    stats += str(weak_components) + ' weak components\n'
    stats += str(cutvertices) + ' cut vertices'
    print(stats)
    fout.write(stats)
    fout.write('\n')
    help = [
        0.0001, 0.001, 0.01, 1, 
        10, 100, 1000, 10000
    ]
    t = len(help)
    getters = [0 for i in range(t + 1)]
    givers = [0 for i in range(t + 1)]
    balance_stats = [0 for i in range(t + 1)]
    for i in G.vs['received']:
        j = 0
        while j < t and i > help[j]:
            j += 1
        getters[j] += 1
    for i in G.vs['gave']:
        j = 0
        while j < t and i > help[j]:
            j += 1
        givers[j] += 1    
    help = list(map(str, help))
    getters = list(map(str, getters))
    givers = list(map(str, givers))
    balance_stats = list(map(str, balance_stats))
    fout.write(
        '# nodes that received < ' + help[0] + value + ':' + getters[0] + '\n'
    )
    for i in range(t - 1):
        fout.write(
            '# nodes that received >' + help[i] +  value + 'and < ' + 
            help[i + 1] + value + ':' + getters[i + 1] + '\n'
        )
    fout.write(
        '# nodes that received > ' + help[t - 1] 
        + value + ':' + getters[-1] + '\n'
    )
    fout.write('\n')
    fout.write('# nodes that gave < ' + 
          help[0] +  value + givers[0] + '\n')
    for i in range(t - 1):
        fout.write(
            '# nodes that gave > ' + help[i] + value + 'and < ' 
            + help[i + 1] + value + ':' + givers[i + 1] + '\n'
        )
    fout.write(
        '# nodes that gave > ' + help[t - 1] + givers[-1] + '\n'
    )
    fout.write('\n')
    help = [-1000, -100, -10, -1, 0, 1, 10, 100, 1000]
    balance_stats = [0 for i in range(len(help))]
    balance = [G.vs[i]['received'] - G.vs[i]['gave'] for i in range(G.vcount())]
    for i in balance:
        j = 0
        while j < t and i > help[j]:
            j += 1
        balance_stats[j] += 1    
    help = list(map(str, help))
    fout.write(
        '# nodes whose balance is  < ' + help[0] 
        + value + ':' + getters[0] + '\n'
    )
    for i in range(t - 1):
        fout.write(
            '# whose balance is >' + help[i] +  value 
            + 'and < ' + help[i + 1] + value + ':' + getters[i + 1] + '\n'
        )
    fout.write('# nodes whose balance is > ' + 
          help[t - 1] + value + ':' + getters[-1] + '\n')
    help = [1, 5, 10, 50, 100, 500, 1000]
    t = len(help)
    cluster_stats = [[0, 0] for i in range(t + 1)]
    for cluster in G.clusters(mode='WEAK'):
        i = len(cluster)
        j = 0
        while j < t and i > help[j]:
            j += 1
        cluster_stats[j][0] += 1    
        cluster_stats[j][1] += i    
    help = list(map(str, help))
    fout.write(
        '# connected components with <' + help[0] + ' vertices: ' 
        + str(cluster_stats[0][0]) + '; ' + str(cluster_stats[0][1])  
        + ' vertices\n'
    )
    for i in range(t - 1):
        fout.write(
            '# connected components with >' + help[i] + ' vertices ' 
            + 'and <' + help[i + 1] + ' vertices: '
            + str(cluster_stats[i + 1][0]) + '; ' + str(cluster_stats[i + 1][1])  
            + ' vertices\n'
        )
    fout.write(
        '# connected components with >' + 
        help[t - 1] + ' vertices: ' + str(cluster_stats[-1][0]) + '; ' 
        + str(cluster_stats[-1][1])  + ' vertices'  + '\n'
    )
    fout.write('\n')
    top_givers = []
    top_receivers = []
    A = [(G.vs[i]['gave'], i) for i in range(G.vcount())]
    B = [(G.vs[i]['received'], i) for i in range(G.vcount())]
    A.sort(reverse=True)
    B.sort(reverse=True)
    fout.write('top givers:\n')
    for i in range(10):
        fout.write(
            str(i) 
            + '. ' + G.vs[A[i][1]]['addr'] + ' ' 
            + str(G.vs[A[i][1]]['gave']) + '\n'
        )
    fout.write('\n')
    fout.write('top receivers:\n')
    for i in range(10):
        fout.write(
            str(i) 
            + '. ' + G.vs[B[i][1]]['addr'] + ' ' 
            + str(G.vs[B[i][1]]['received']) + '\n'
        )   
    fout.write('\n')
    C = [(G.vs[i].degree(), i) for i in range(G.vcount())]
    C.sort(reverse=True)
    fout.write('top interactors:\n')
    for i in range(12):
        fout.write(
            str(i) 
            + '. ' + G.vs[C[i][1]]['addr'] + ' ' 
            + str(G.vs[C[i][1]].degree()) + '\n'
        )
    fout.close()