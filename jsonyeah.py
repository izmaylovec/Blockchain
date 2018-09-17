import requests
import copy
import time
import shelve
import json


#def BlockPars(Hash):


    #headers = {
        #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    #}
    #r = requests.get('https://blockchain.info/rawblock/' + Hash, headers=headers)

    #html_code = r.text
    #return html_code

#a = open('tmp.txt', 'w')
#a.write(BlockPars(input()))
#a.close()

G = ig.Graph(directed=True)

fin = open('block0000000000000000000cb2e17c8cab5e9bd56312faf411a52f1be606717652b6.json')
a = fin.read()
wow = json.loads(a)
vertex_in_graph_by_addr = dict()
edge_in_graph_by_addr = dict()
edges = set()
to_add = []
attr = []
for transaction in wow['tx']:
    if len(tx.input_keys) > 1:
        multitransactions += 1  
    if tx.input_keys != [keY('No Inputs (Newly Generated Coins)')]:
        for j in range(len(tx.input_keys)): # adding vertex to the graph, first iterating the input_keys
            key = tx.input_keys[j]
            address, name = key.address, key.name
            #print(address, name)
            if sys.intern(address) not in vertex_in_graph_by_addr:                          
                vertex_in_graph_by_addr[sys.intern(address)] = vertex_number
                G.add_vertex()
                G.vs[vertex_number]['addr'] = address
                G.vs[vertex_number]['gave'] = get_number(tx.input_value[j])
                G.vs[vertex_number]['received'] = 0
                G.vs[vertex_number]['name'] = name
                vertex_number += 1
            else:
                G.vs[vertex_in_graph_by_addr[sys.intern(address)]]['gave'] += get_number(tx.input_value[j])
            
            
    for j in range(len(tx.output_keys)): # adding vertex to the graph, iterating the output_keys  
        address, name = tx.output_keys[j].address, tx.output_keys[j].name
        if sys.intern(address) not in vertex_in_graph_by_addr:
            vertex_in_graph_by_addr[sys.intern(address)] = vertex_number
            G.add_vertex()
            G.vs[vertex_number]['addr'] = address
            G.vs[vertex_number]['received'] = get_number(tx.output_value[j])
            G.vs[vertex_number]['gave'] = 0
            G.vs[vertex_number]['name'] = name
            vertex_number += 1
        else:
            G.vs[vertex_in_graph_by_addr[sys.intern(address)]]['received'] += get_number(tx.output_value[j])
            
    for j in range(len(tx.input_keys)): # adding edges according to the current transacion
        for k in range(len(tx.output_keys)):
            inp = tx.input_keys[j].address
            outp = tx.output_keys[k].address
            if (vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp]) not in edges:
                to_add.append((vertex_in_graph_by_addr[outp], vertex_in_graph_by_addr[inp]))
                edges.add((vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp]))
                edge_in_graph_by_addr[(vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp])] = edge_number
                attr.append(tx.date + ' ' + tx.output_value[k] + '#')
                edge_number += 1
            else:              
                number_edge = edge_in_graph_by_addr[(vertex_in_graph_by_addr[inp], vertex_in_graph_by_addr[outp])]
                attr[number_edge] += tx.date + ' ' + tx.output_value[k] + '#'
                
G.add_edges(to_add)
G.es['tx'] = attr
print('here')
G.write_pickle(filename + ' aug graph.txt')    
fin.close()