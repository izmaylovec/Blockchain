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

filename = '06 aug blocks'

fin = open('blocks/' + filename + '.txt')

Data = fin.read().split('\n')
Hash = '0000000000000000000cb2e17c8cab5e9bd56312faf411a52f1be606717652b6'
for i in range(10):
    print(i)
    Hash = Data[i][-64:]
    html_code = requests.get('https://blockchain.info/rawblock/' + Hash).text
    
    fout = open('block' + Hash + '.json', 'w')
    fout.write(html_code)
    wow = json.loads(html_code)
    Hash = wow['prev_block']
    fout.close()