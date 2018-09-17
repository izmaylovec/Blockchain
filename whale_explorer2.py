from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import requests
import bs4
from bs4 import BeautifulSoup
import urllib3
import queue
urllib3.disable_warnings()
import time


def get_number(value):
    return float(value[:-3].replace(',', ''))
    

fin = open('whale0.txt')
Data = fin.read().split('#')
size = int(Data[0])
value = float(Data[1])
addresses = ['1HXg4ec4rGfNNTAr4jtzSVfeW5XF2nq4ud']
q = queue.Queue()
used = set()
for address in addresses:
    if address != '':
        q.put(address)
    #used.add(address)
print('here')
fout = open('whale0txup.txt', 'a')
fout2 = open('whale0addr_info4.txt', 'a')

fin_saved_urls = open('saved_urls2.txt')
saved_urls = set(fin_saved_urls.read().split('\n'))
fin_saved_urls.close()

tx_number = 0
count = time.clock()
counter = 0
while not q.empty() and time.clock() - count < 300 and counter < 300: # working with the element from queue
    counter += 1
    print(counter)
    address = q.get()
    
    addr = address[:34]
    
    url = 'https://www.blockchain.com/ru/btc/address/' + addr
    if False:
        fin_url = open(addr + '.txt', encoding = 'utf8')
        soup = BeautifulSoup(fin_url.read(), "html.parser")
        fin_url.close()
    else:
        soup = BeautifulSoup(get(url, verify=False).text, "html.parser")
        time.sleep(0.01)
        #fout_to_save = open(addr + '.txt', 'w+', encoding = 'utf8')
        #fout_to_save.write(str(soup))
        #fout_to_save.close()
        #fout_saved_urls = open('saved_urls.txt', 'a')
        #fout_saved_urls.write(url + '\n')
        #fout_saved_urls.close()
        #saved_urls.add(url)
    
    specific_name = soup.find('h1').text[:-94]
    n_transactions = soup.find(attrs = {"id":"n_transactions"}).text
    total_received = soup.find(attrs = {"id":"total_received"}).text
    final_balance = soup.find(attrs = {"id":"final_balance"}).text
    fout2.write(specific_name + ';\n address: ' + 
                address + ';\n n_transactions:' + 
                n_transactions + ';\n total_received ' + 
                total_received + ';\n final_balance ' + final_balance + '\n\n')            
    offset = 0 #
    while offset < 50:
        url = 'https://www.blockchain.com/ru/btc/address/' 
        url += addr + '?offset=' + str(offset) + '&filter=2&sort=1'
        if False:
            fin_url = open(addr + '.txt', encoding = 'utf8')
            soup = BeautifulSoup(fin_url.read(), "html.parser")
            fin_url.close()
        else:
            soup = BeautifulSoup(get(url, verify=False).text, "html.parser")
            #fout_to_save = open(url + '.txt', 'w+', encoding = 'utf8')
            #fout_to_save.write(str(soup))
            #fout_to_save.close()
            #fout_saved_urls = open('saved_urls.txt', 'a')
            #fout_saved_urls.write(url + '\n')
            #fout_saved_urls.close()
            #saved_urls.add(url)
        transactions = soup.find_all(attrs={'class':'txdiv'})                
        for i in range(min(len(transactions),2)):
            transaction = transactions[i]
            raw = transaction.table.find_all('tr')
            hash_date = raw[0]
            hash_ = hash_date.th.a.text
            date = hash_date.th.span.text
            abc = raw[1].find_all('td')
            gett = (abc[1].img.get('src') == '/Resources/arrow_right_green.png')
            inp_write_txt = '' # this is for writing to the txt file
            inp_write_queue = [] # this is for queue
            inputs = abc[0].contents
            for j in range(len(inputs)): # doing job with input addresses
                t = inputs[j]
                if type(t) == bs4.element.NavigableString:
                    print(hash_, t)
                    #inp_write_txt += t + '\n' 
                    inp_write_queue.append(t) 
                else:
                    t = t.text
                    
                    #inp_write_txt += t + '\n'
                    inp_write_queue.append(t) 
            outputs = abc[2].contents
            i = 0
            value_txt = [] # for writing to txt file
            value_number = 0
            outp_write_txt = ''
            outp_write_queue = []
            while i < len(outputs): # dealing with output addresses
                while str(outputs[i]) != '<br/>':
                    i += 1
                value_number += get_number(outputs[i - 1].text)
                value_txt.append(outputs[i - 1].text)
                if outputs[i - 2] != ' ':
                    s = outputs[i - 2]
                else:
                    s = outputs[i - 3].text
                #outp_write_txt += s + '\n'
                outp_write_queue.append(s)
                i += 1                      
            fout.write(hash_ + '\n#\n' + date + '\n#\n') # writing transaction to txt file
            fout.write('\n'.join(inp_write_queue) + '\n#\n')
            fout.write('\n'.join(outp_write_queue) + '\n')
            fout.write('#\n' + '\n'.join(value_txt))
            fout.write('\n\n\n') 
            for s in inp_write_queue[:1]: # putting the ancestors to the queue
                print(s)
                if s not in used and len(s) > 32:
                    #print(s)
                    q.put(s)
                    used.add(s)
            #for s in outp_write_queue: # putting the ancestors to the queue
                #if s not in used and len(s) == 34:
                    #pass
                    #print(s)
                    #q.put(s)
                    #used.add(s)                
            tx_number += 1
        offset += 50
        

fin.close()
fout.close()
fout2.close()

fout = open('whale03left.txt', 'w')
fout.write('###')
a = []
while not q.empty():
    a.append(q.get())
fout.write('@'.join(a))
fout.close()