import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import time
import igraph as ig
import pickle
from math import log, sin, cos, sqrt

plotly.tools.set_credentials_file(username='avalokiteshvara', api_key='f6W73HfccvtBbHn8BqZt')


def clusterize(G):
    C = G.biconnected_components()
    membership = [0 for i in range(G.vcount())]
    for i in range(len(C)):
        for j in C[i]:
            membership[j] = i
    D = ig.clustering.VertexClustering(G, membership)
    E = D.cluster_graph()    
    return E
    
    
def prettify(G): # gets rid of small connected components    
    C = G.clusters(mode='WEAK')
    E = G
    to_delete = []
    for cluster in C:
        if len(cluster) < 5:
            to_delete += cluster
    E.delete_vertices(to_delete)
    return E


def rotate(x, y, alpha):
    return x * cos(alpha) - y * sin(alpha), x * sin(alpha) + y * cos(alpha)
    
    
G = ig.Graph.Read_Pickle('graph_data_ether_100000.txt')
fin = open('statistics_ether_100000.txt')
Text = fin.read()
count = time.clock()
N = G.vcount()
B = G.clusters(mode='WEAK')
A = B.subgraphs()
n = len(A)
layts = []
diams = []
for i in range(n):
    subgraph = A[i]
    layt = subgraph.layout_auto(dim=3)    
    min_x, max_x, min_y, max_y, min_z, max_z = 0, 0, 0, 0, 0, 0
    for x, y, z in layt:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)
    diams.append((max(max_x - min_x, max_y - min_y, max_z - min_z), i))
    layts.append((max(max_x - min_x, max_y - min_y, max_z - min_z), layt))
layts.sort(reverse=True)
diams.sort(reverse=True)
sums = [0 for i in range(n)]
sums[0] = diams[0][0]
for i in range(1, n):
    sums[i] = sums[i - 1] + diams[i][0]
mode='hexagonal'
if mode == 'circles':
    beg = 0
    end = n
    radius = 0
    while end != 1:
        print(end)
        beg = 0
        End = end
        while beg != end - 1:
            m = (beg + end) // 2
            if sums[m] < sums[End - 1] - sums[m]:
                beg = m
            else:
                end = m
        length = sums[End - 1] - sums[end - 1]
        R = length / (2 * 3.1416)
        radius = max(R, radius)
        gone = 0
        for i in range(end, End):
            alpha = gone / length * 2 * 3.1416
            for j in range(len(layts[i][1])):
                x, y, z = layts[i][1][j]
                x, y = rotate(x + R, y + R, alpha)
                layts[i][1][j] = x, y, z
            gone += diams[i][1] / 2 + diams[(i + 1) % n][1] / 2    
elif mode == 'hexagonal':
    grid = []
    placed = 0
    number = 0
    coords = [0, 0]
    radius = 0
    to_plus = [
        (-0.5, sqrt(3) / 2), (-1, 0), (-0.5, -sqrt(3) / 2),
        (0.5, -sqrt(3) / 2), (1, 0), (0.5, sqrt(3) / 2)
    ]
    while placed != n:
        coords[0] += diams[placed][0] / 2 + diams[placed - 6 * (number)][0] / 2
        mul = coords[0] / (number + 1)
        print(placed, number)
        for i in range(6):    
            for j in range(number + 1):
                if placed != n:
                    for k in range(len(layts[placed][1])):
                        x, y, z = layts[placed][1][k]
                        x, y = x + coords[0], y + coords[1]
                        layts[placed][1][k] = x, y, z                
                    coords[0] += to_plus[i][0] * mul
                    coords[1] += to_plus[i][1] * mul
                    placed += 1
        number += 1
    radius = sqrt(coords[0] * coords[0] + coords[1] * coords[1])

layt = [[] for i in range(G.vcount())]        
for i in range(n):
    for j in range(len(B[diams[i][1]])):
        layt[B[diams[i][1]][j]] = layts[i][1][j]
#layt = G.layout_fruchterman_reingold(dim=3, maxiter=20)
Xn = [layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn = [layt[k][1] for k in range(N)]# y-coordinates
Zn = [layt[k][2] for k in range(N)]# z-coordinates
Xe_inp, Ye_inp, Ze_inp, Xe_outp, Ye_outp, Ze_outp = [], [], [], [], [], []
Xnm, Ynm, Znm = [], [], []
adj_list = G.get_adjlist()
for i in range(len(adj_list)):
    for j in range(len(adj_list[i])):
        Xe_outp += [
            (layt[i][0] + layt[adj_list[i][j]][0]) / 2, 
            layt[adj_list[i][j]][0], 
            None
        ]
        Ye_outp += [
            (layt[i][1] + layt[adj_list[i][j]][1]) / 2, 
            layt[adj_list[i][j]][1], 
            None
        ]
        Ze_outp += [
            (layt[i][2] + layt[adj_list[i][j]][2]) / 2, 
            layt[adj_list[i][j]][2], 
            None
        ]
        Xe_inp += [
            layt[i][0], 
            (layt[i][0] + layt[adj_list[i][j]][0]) / 2, 
            None
        ]
        Ye_inp += [
            layt[i][1], 
            (layt[i][1] + layt[adj_list[i][j]][1]) / 2, 
            None
        ]
        Ze_inp += [
            layt[i][2], 
            (layt[i][2] + layt[adj_list[i][j]][2]) / 2, 
            None
        ]
        Xnm.append((layt[i][0] + layt[adj_list[i][j]][0]) / 2)
        Ynm.append((layt[i][1] + layt[adj_list[i][j]][1]) / 2)
        Znm.append((layt[i][2] + layt[adj_list[i][j]][2]) / 2)
max_gave, max_received = max(G.vs['gave']), max(G.vs['received'])
min_gave, min_received = max_gave, max_received
for i in range(N):
    if 0 < G.vs[i]['gave'] < min_gave:
        min_gave = G.vs[i]['gave']
    if 0 < G.vs[i]['received'] < min_received:
        min_received = G.vs[i]['received']
size_gave = [0 for i in range(N)]
size_received = [0 for i in range(N)]
for i in range(N):
    gave, received = G.vs[i]['gave'], G.vs[i]['received']
    if gave == 0:
        size_gave[i] = 0
    elif gave == min_gave:
        size_gave[i] = 1
    else:
        size_gave[i] = log(gave/min_gave) 
    if received == 0:
        size_received[i] = 0
    elif received == min_received:
        size_received[i] = 1
    else:
        size_received[i] = log(received/min_received)
edges_inp=go.Scatter3d(
    x=Xe_inp,
    y=Ye_inp,
    z=Ze_inp,
    mode='lines',
    line=dict(color='rgb(255,0,0)', width=1),
    hoverinfo='skip',
    showlegend=False,                   
)
edges_outp=go.Scatter3d(
    x=Xe_outp,
    y=Ye_outp,
    z=Ze_outp,
    mode='lines',
    line=dict(color='rgb(0,255,0)', width=1),
    hoverinfo='skip',
    showlegend=False
)
mid=go.Scatter3d(
    x=Xnm,
    y=Ynm,
    z=Znm,
    mode='markers',
    name = 'info about transactions',
    marker=dict(
        symbol='circle',
        size=1, 
        color='rgb(255,0,102)',
        line=dict(color='rgb(255,0,0)'), 
        width=0.5
    ),
    text = G.es['tx'],
    hoverinfo = 'text+name'
)
nodes_inp=go.Scatter3d(
    x=Xn,
    y=Yn,
    z=Zn,
    mode='markers',
    name = 'the bigger - the more node received',
    marker=dict(
        symbol='circle',
        size=size_gave, 
        color='rgb(255,0,0)',
        line=dict(
            color='rgb(255,0,0)', 
            width=0.5
        )
    ),
    text = G.vs['gave'],
    hoverinfo = 'text+name'
)
nodes_outp=go.Scatter3d(x=Xn,
    y=Yn,
    z=Zn,
    mode='markers',
    name = 'the bigger - the more node gave',
    marker=dict(
        symbol='circle',
        size=size_received, 
        color='rgb(0,255,0)',
        line=dict(
            color='rgb(0,255,0)', 
            width=0.5
        )
    ),
    text = G.vs['received'],
    hoverinfo = 'text+name'
)    
nodes=go.Scatter3d(
    x=Xn, 
    y=Yn, 
    z=Zn, 
    mode='markers', 
    name = 'just nodes',
    marker=dict(
        symbol='circle',
        size=1,                                
        colorscale='Viridis',
        line=dict(color='rgb(50,50,50)', 
                  width=0.5
        )
    ),
    text = G.vs['addr'], 
    hoverinfo = 'text+name'
)
axis=dict(
    showbackground=True,
    showline=False,
    zeroline=True,
    showgrid=True,
    showticklabels=True,
    title='',
    range=(-2 * radius, 2 * radius)
)
layout = go.Layout(
    title="graph of ethereum transactions",
    width=1000,
    height=1000,
    showlegend=True,     
    scene=dict(
        xaxis=dict(axis),
        yaxis=dict(axis),
        zaxis=dict(axis),
        aspectmode='cube',
    ),
    margin=dict(
        autoexpand=True
    ), 
    hovermode='closest',
    annotations=[
        dict(
            showarrow=False,text=Text.replace('\n', '<br>'),
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='right',
            yanchor='bottom',
            align='left',
            font=dict(
                size=12
            )
        )
    ],    
)

data=[edges_inp, edges_outp, nodes_inp, nodes_outp, nodes, mid]
fig=go.Figure(data=data, layout=layout)

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
plot(fig, filename = 'ether100000')
print('here', time.clock() - count)
#py.plot(fig, filename='another experiment 17 aug, 6 aug', autorun=True)