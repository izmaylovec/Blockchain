fin = open("transactions/06 aug transactions full correct.txt", encoding = 'cp1251')

a = set()
Data = fin.read().split('\n')
for line in Data:
    if len(line) not in [0, 1, 19, 33, 34, 35, 36, 38, 42, 43,62, 64] and line[-3:] != 'BTC':
        #print(line)
        a.add(line)
for line in a:
    print(line)
fin.close()