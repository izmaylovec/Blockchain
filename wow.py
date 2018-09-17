import igraph as ig

G = ig.Graph.Read_Pickle('08 aug transactions.txt')
G.write('08 aug graph.gml', format='gml')
