fin = open("parce_top100richest.txt")
Data = fin.readlines()
last_enter_addr = dict()
last_enter_value = dict()
for addr in Data:
    print(addr)
    if addr != '':
        addr = addr[:-1].split('#')
        if addr[5] not in last_enter_addr.keys():
            last_enter_addr[addr[5]] = [addr[1]]
            last_enter_value[addr[5]] = float(addr[2].replace(',', '').split('BTC')[0])
        else:
            last_enter_addr[addr[5]].append(addr[1])
            last_enter_value[addr[5]] += float(addr[2].replace(',', '').split('BTC')[0])


A = []
for key in last_enter_addr.keys():
    
    A.append([len(last_enter_addr[key]), last_enter_value[key], key, last_enter_addr[key]])

fout = open('richest_clusters.txt', 'w')

A.sort(key=lambda x: x[1], reverse=True)
for a, b, c, d in A:
    print(a, b, c, d)
    fout.write('#'.join(list(map(str, [a, b, c, '@'.join(d)]))) + '\n')
fout.close()
for i in range(6):
    name = 'whale' + str(i) + '.txt'
    fout = open(name, 'w')
    a, b, c, d = A[i]
    fout.write('#'.join(list(map(str, [a, b, c, '@'.join(d)]))) + '\n')
    fout.close()
