#coding = utf8

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import time
import igraph as ig
import pickle
from math import log
import sys
import queue


class transaction:
    
    def __init__(self, piece):
        tx = piece.split('\n#\n')    
        #print(len(tx))
        if len(tx) == 4:
            #print(tx[0],tx[1], tx[2], tx[3], sep='\n')
            a = tx[3].split('#')
            tx[3] = a[0]
            #print(a)
            tx.append(a[1])
        self.Hash = tx[0]
        self.date = tx[1]
        a = list(map(lambda x: x[:34], tx[2].split('\n\n')))
        self.input_keys = []
        for s in a:
            if len(s) == 34:
                self.input_keys.append(s)
        a = list(map(lambda x: x[:34], tx[3].split('\n')))
        self.output_keys = []
        for s in a:
            if len(s) == 34:
                self.output_keys.append(s)
        
        self.value = tx[4].split('\n')
        
    
    def loop(self):
        return set(self.input_keys) == set(self.output_keys)

    
    def __str__(self):
        return (self.date + 
                '\n'.join(self.value) +'\n\n\n')


    def get_number(value):
        if value[-3:] == 'BTC':
            return float(value[:-3].replace(',', ''))
        elif value[-5:] == 'Ether':
            
            return float(value[:-5].replace(',', ''))
        else:
            return 0


count = time.clock()
folder = 'transactions/'
filename = '06 aug transactions full correct'
filetowrite = filename + time.asctime() +  'vis2d.html'
fin = open(folder + filename + '.txt', encoding = 'cp1251') #reading the file
Data = fin.read().split('\n\n\n')
print(len(Data))
vertex = set()  
edges = list()
number = len(Data) - 1 # how many transactions are included in the graph
value_generation_tx = 0  # #transactions, in which new bitcoins are generated
loops = 0 # #transactions, in which user sends money to himself
multitransactions = 0 # #transactions, which have > one input key

G = ig.Graph(directed=True)
mode = ''
vertex_number = 0
edge_number = 0
vertex_in_graph_by_addr = dict()
edge_in_graph_by_addr = dict()
edges = set()
to_add = []
attr = []
to_add_ = []
for i in range(number - 1):  # creating the graph by iterating all transactions
    #print(i, time.clock() - count)
    tx = transaction(Data[i])
    if tx.input_keys == ['��� ������� ������ (����� ������)']:
        value_generation_tx += 1
    elif tx.loop():
        loops += 1
    else:
        if len(tx.input_keys) > 1:
            multitransactions += 1            
        for address in tx.input_keys: # adding vertex to the graph, first iterating the input_keys            
            if sys.intern(address) not in vertex_in_graph_by_addr:
                vertex_in_graph_by_addr[sys.intern(address)] = vertex_number
                G.add_vertex()
                G.vs[vertex_number]['addr'] = address
                G.vs[vertex_number]['gave'] = sum(list(map(get_number, tx.value)))
                G.vs[vertex_number]['received'] = 0
                vertex_number += 1
            else:
                G.vs[vertex_in_graph_by_addr[sys.intern(address)]]['gave'] += sum(list(map(get_number, tx.value)))
                
        for j in range(len(tx.output_keys)): # adding vertex to the graph, iterating the output_keys  
            address = tx.output_keys[j]
            if sys.intern(address) not in vertex_in_graph_by_addr:
                h = time.clock()
                vertex_in_graph_by_addr[sys.intern(address)] = vertex_number
                G.add_vertex()
                G.vs[vertex_number]['addr'] = address
                G.vs[vertex_number]['received'] = get_number(tx.value[j])
                G.vs[vertex_number]['gave'] = 0
                vertex_number += 1
            else:
                G.vs[vertex_in_graph_by_addr[sys.intern(address)]]['received'] += get_number(tx.value[j])
        
        for inp in tx.input_keys: # adding edges according to the current transacion
            for j in range(len(tx.output_keys)):
                outp = tx.output_keys[j]
                
                if inp == '1N8emyFpMob6hDVhLiV1kTPiHBB8DQHWpp' and outp == '1DDHzSGfdW6eXkVZNzak6osvt2ujJu5Q45':
                    print('here', (vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp]), (vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp]) in edges)
                
                if (vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp]) not in edges:
                    to_add.append((vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp]))
                    to_add_.append((vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp]))
                    edges.add((vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp]))
                    edge_in_graph_by_addr[(vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp])] = edge_number
                    attr.append(tx.date + ' ' + tx.value[j] + '#')
                    edge_number += 1
                else:
                    number_edge = edge_in_graph_by_addr[(vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp])]
                    attr[number_edge] += tx.date + ' ' + tx.value[j] + '#'

                
G.add_edges(to_add)                
G.es['tx'] = attr
G_ = ig.Graph(G.vcount())
G_.add_edges(to_add_)
if mode == 'customlayers':
    layers = [0 for i in range(G.vcount())]
    whale = open('whale0.txt')
    Data = whale.read().split('#')
    whale.close()
    size = int(Data[0])
    value = float(Data[1])
    addresses = list(Data[3].split('@'))
    start = [vertex_in_graph_by_addr['18tTLso5jaa4XqyTQzo9S6mqhfCsgcufdh']]
    q = queue.Queue()
    for v in start:
        q.put((0, v))
    
    used = [False for i in range(G.vcount())]
    
    while not(q.empty()):
        layer, vertex = q.get()
        if not used[vertex]:
            print(layer, vertex, G.vs[vertex]['gave'], G.vs[vertex]['received'], len(G.neighbors(vertex)))
            layers[vertex] = layer
            used[vertex] = True
            for Id in G.neighbors(vertex, mode='IN'):
                if not used[Id]:
                    #print(layer + 1, Id)
                    q.put((layer + 1, Id))
            for Id in G.neighbors(vertex, mode='OUT'):
                if not used[Id]:
                    q.put((layer - 1, Id))    
            used[vertex] = True


Text = ''
count = time.clock()
N = G.vcount()

layts = []

print('here')
if mode == 'customlayers':
    layt = G.layout_sugiyama(layers, maxiter=10000, hgap = 10)
else:
    layt = G.layout_sugiyama(maxiter=10000, hgap = 10)
Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Xe_inp, Ye_inp, Xe_outp, Ye_outp = [], [], [], []
Xnm, Ynm = [], []
adj_list = G.get_adjlist()
for i in range(len(adj_list)):
    for j in range(len(adj_list[i])):
        Xe_outp += [(layt[i][0] + layt[adj_list[i][j]][0]) / 2, layt[adj_list[i][j]][0], None]
        Ye_outp += [(layt[i][1] + layt[adj_list[i][j]][1]) / 2, layt[adj_list[i][j]][1], None]
        Xe_inp += [layt[i][0], (layt[i][0] + layt[adj_list[i][j]][0]) / 2, None]
        Ye_inp += [layt[i][1], (layt[i][1] + layt[adj_list[i][j]][1]) / 2, None]
        Xnm.append((layt[i][0] + layt[adj_list[i][j]][0]) / 2)
        Ynm.append((layt[i][1] + layt[adj_list[i][j]][1]) / 2)
        
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
edges_inp=go.Scatter(x=Xe_inp,
               y=Ye_inp,
               mode='lines',
               line=dict(color='rgb(255,0,0)', width=1),
               hoverinfo='skip',
               showlegend=False,                   
               )

edges_outp=go.Scatter(x=Xe_outp,
               y=Ye_outp,               
               mode='lines',
               line=dict(color='rgb(0,255,0)', width=1),
               hoverinfo='skip',
               showlegend=False
               )

mid=go.Scatter(x=Xnm,
           y=Ynm,
           mode='markers',
           name = 'info about transactions',
           marker=dict(symbol='circle',
                         size=1, 
                         color='rgb(255,0,102)',
                         line=dict(color='rgb(255,0,0)', width=0.5)
                         ),
          
           text = G.es['tx'],
           hoverinfo = 'text+name'
           )
nodes_inp=go.Scatter(x=Xn,
               y=Yn,
               mode='markers',
               name = 'the bigger - the more node gave',
               marker=dict(symbol='circle',
                             size=size_gave, 
                             color='rgb(255,0,0)',
                             line=dict(color='rgb(255,0,0)', width=0.5)
                             ),
               text = G.vs['gave'],
               hoverinfo = 'text+name'
               )

nodes_outp=go.Scatter(x=Xn,
               y=Yn,          
               mode='markers',
               name = 'the bigger - the more node received',
               marker=dict(symbol='circle',
                             size=size_received, 
                             color='rgb(0,255,0)',
                             line=dict(color='rgb(0,255,0)', width=0.5)
                             ),
              
               text = G.vs['received'],
               hoverinfo = 'text+name'
               )    

nodes=go.Scatter(x=Xn, y=Yn, mode='markers', name = 'just nodes',
               marker=dict(symbol='circle',
                             size=1,                                
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text = G.vs['addr'], hoverinfo = 'text+name'
               )

#dont know
axis=dict(showbackground=True,
          showline=False,
          zeroline=True,
          showgrid=True,
          showticklabels=True,
          title='',
          )

layout = go.Layout(
         title="graph of ethereum transactions",
         width=20000,
         height=1000,
         showlegend=True,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             aspectmode='cube',
        ),
     margin=dict(
        #autoexpand=True
    ),
     
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text=Text.replace('\n', '<br>'),
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
        ],    )

data=[edges_inp, edges_outp, nodes_inp, nodes_outp, nodes, mid]
fig=go.Figure(data=data, layout=layout)
print("here")
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
plot(fig, filename = filetowrite)