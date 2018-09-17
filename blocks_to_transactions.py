from requests import get
import bs4
from bs4 import BeautifulSoup
import urllib3
import time


def prettify(s):
    return str(round(float(s.replace(',', '')) / 1000, 10))

            
def get_number(value):
    if value.endswith('BTC'):
        return float(value[:-3].replace(',', ''))
    elif value.endswith('Ether'):
        return float(value[:-5].replace(',', ''))
    else:
        return 0


to_write = []
for date in range(24, 31):
    print(date)
    fin = open(str(date) + ' aug.txt')
    urls = fin.read().split('\n')
    print(len(urls))
    fout = open(str(date).rjust(2, '0') 
                + ' aug transactions full correct.txt', 'w')
    #fout = open('bwa.txt', 'w')
    count = time.clock()
    for k in range(len(urls) - 1):
        url = urls[k]
        print(k, time.clock()-count)
        link = get(url.replace('/ru', '/en') + '?show_adv=true&currency=MBC').text
        soup = BeautifulSoup(link, 'html.parser') 
        transactions = soup.find_all(attrs={'class':'txdiv'})                
        for i in range(len(transactions)):
            transaction = transactions[i]
            raw = transaction.table.find_all('tr')
            hash_date = raw[0]
            hash_ = hash_date.th.a.text
            date = hash_date.th.span.text[-19:]
            info = hash_date.th.span.text[:-19]
            abc = raw[1].find_all('td')
            inp_write_txt = '' # this is for writing to the txt file
            inp_write_queue = [] # this is for queue
            value_txt_inp = []
            if abc[0].text == 'No Inputs (Newly Generated Coins)':
                inp_write_queue = ['No Inputs (Newly Generated Coins)']
            else:
                inputs = abc[0].text.split(' - Output)')               
                for i in range(len(inputs) - 1):
                    line = inputs[i]
                    l = line.split(' (')
                    key, value = l[0], l[-1].split(')')[-1]
                    if len(l) > 2:
                        key += ' $ ' + l[1]
                    inp_write_queue.append(prettify(key))
                    value_txt_inp.append(prettify(value[:-4]))
            outputs = abc[2].text.split(' mBTC')
            outputs.pop()
            i = 0
            value_txt = [] # for writing to txt file
            value_number = 0
            outp_write_txt = ''
            outp_write_queue = []
            for line in outputs:
                l = line.split('(')
                key, value = l[0].split('-')[0], l[-1].split(')')[-1]
                if len(l) > 2:
                    key += ' $ ' + l[1].split(')')[0] 
                outp_write_queue.append(key.strip(' ()'))
                value_txt.append(prettify(value))            
            to_write.extend([hash_ + '\n#\n' + date + '\n#\n',
                             info + '\n#\n',
                             '\n'.join(inp_write_queue) + '\n#\n',
                             ' BTC\n'.join(value_txt_inp) + ' BTC\n#\n',
                             ' BTC\n'.join(value_txt) + ' BTC',
                             '\n\n\n'
                             ])
            
    fout.write(''.join(to_write))    
    fin.close()
    fout.close()