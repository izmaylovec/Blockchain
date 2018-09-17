import time
import igraph as ig
import pickle
import sys


class keY:
    
    def __init__(self, s):
        if '$' in s:
            self.address, self.name = s.split(' $ ')
        elif '1' in s or '2' in s or '3' in s:
            self.address, self.name = s, ''
        else:
            self.address, self.name = '', s
            
        
    def __eq__(self, other):
        return self.name == other.name and self.address == other.address
        

class transaction:
    
    def __init__(self, piece):
        tx = piece.split('\n#\n')      
        self.Hash = tx[0]
        self.date = tx[1]
        self.info = tx[2]
        self.inp_keys = list(map(lambda s: keY(s), tx[3].split('\n')))
        self.inp_val = tx[4].split('\n')
        self.out_keys = list(map(lambda s: keY(s), tx[5].split('\n')))
        self.out_val = tx[6].split('\n')
    
    def __str__(self):
        return (self.date + '\n'.join(self.value) +'\n\n\n')


def get_num(value):
    if value.endswith('BTC'):
        return float(value[:-3].replace(',', ''))
    elif value.endswith('Ether'):
        return float(value[:-5].replace(',', ''))
    else:
        return 0


count = time.clock()
folder = 'transactions/'
for filename in [
    '09', '10', '11', '12', '13', '24', '25', '26', '27', '28', '29', '30'
    ]:
    fin = open(folder + filename + ' aug transactions full correct.txt')
    #fin = open(folder + filename + '.txt', encoding = 'cp1251') #reading the file
    Data = fin.read().split('\n\n\n')
    vertex = set()  
    edges = list()
    number = len(Data) - 1 # how many transactions are included in the graph
    value_generation_tx = 0  # #transactions, in which new bitcoins are generated
    loops = 0 # #transactions, in which user sends money to himself
    multitransactions = 0 # #transactions, which have > one input key
    
    G = ig.Graph(directed=True)
    vert_num = 0
    edge_num = 0
    vert_by_addr = dict()
    edge_by_addr = dict()
    edges = set()
    to_add = []
    attr = []
    for i in range(number - 1):  
        # creating the graph by iterating all transactions
        tx = transaction(Data[i])
        if len(tx.inp_keys) > 1:
            multitransactions += 1  
        if tx.inp_keys != [keY('No Inputs (Newly Generated Coins)')]:
            # adding vertex to the graph, first iterating the inp_keys
            for j in range(len(tx.inp_keys)): 
                key = tx.inp_keys[j]
                address, name = key.address, key.name
                if sys.intern(address) not in vert_by_addr:                          
                    vert_by_addr[sys.intern(address)] = vert_num
                    G.add_vertex()
                    G.vs[vert_num]['addr'] = address
                    G.vs[vert_num]['gave'] = get_num(tx.inp_val[j])
                    G.vs[vert_num]['received'] = 0
                    G.vs[vert_num]['name'] = name
                    vert_num += 1
                else:
                    G.vs[vert_by_addr[address]]['gave'] += get_num(tx.inp_val[j])               
        for j in range(len(tx.out_keys)): 
            # adding vertex to the graph, iterating the out_keys  
            address, name = tx.out_keys[j].address, tx.out_keys[j].name
            if sys.intern(address) not in vert_by_addr:
                vert_by_addr[sys.intern(address)] = vert_num
                G.add_vertex()
                G.vs[vert_num]['addr'] = address
                G.vs[vert_num]['received'] = get_num(tx.out_val[j])
                G.vs[vert_num]['gave'] = 0
                G.vs[vert_num]['name'] = name
                vert_num += 1
            else:
                G.vs[vert_by_addr[address]]['received'] += get_num(tx.out_val[j])                
        for j in range(len(tx.inp_keys)): 
            # adding edges according to the current transacion
            for k in range(len(tx.out_keys)):
                inp = tx.inp_keys[j].address
                outp = tx.out_keys[k].address
                if (vert_by_addr[inp], vert_by_addr[outp]) not in edges:
                    to_add.append((vert_by_addr[outp], vert_by_addr[inp]))
                    edges.add((vert_by_addr[inp], vert_by_addr[outp]))
                    edge_by_addr[(vert_by_addr[inp], vert_by_addr[outp])] = edge_num
                    attr.append(tx.date + ' ' + tx.out_val[k] + '#')
                    edge_num += 1
                else:              
                    number_edge = edge_by_addr[(vert_by_addr[inp], vert_by_addr[outp])]
                    attr[number_edge] += tx.date + ' ' + tx.out_val[k] + '#'                    
    G.add_edges(to_add)
    G.es['tx'] = attr
    G.write_pickle(filename + ' aug graph.txt')