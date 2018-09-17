from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib3

fout = open('parce_top100richest.txt', 'w')

for i in range(10):
    print(i)
    url = 'https://bitinfocharts.com/ru/top-100-richest-bitcoin-addresses-' + str(i + 1) + '.html'
    soup = BeautifulSoup(get(url).text, "html.parser")
    A = soup.find(attrs={'id':'tblOne'}).find_all('tr') + soup.find(attrs={'id':'tblOne2'}).find_all('tr')
    for data in A:
        data = data.find_all('td')
        for j in range(len(data)):
            data[j] = data[j].text
        fout.write('#'.join(data) + '\n')


fout.close()
    
    