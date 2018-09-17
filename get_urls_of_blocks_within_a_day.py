from requests import get
from bs4 import BeautifulSoup


blocks = '1535108165551'
r = get("https://www.blockchain.com/ru/btc/blocks/" + blocks)
r = r.text
soup = BeautifulSoup(r, "html.parser")
fout = open('24 aug.txt', 'w')
for link in soup.find_all('a'):
    a = link.get('href')
    if len(a) == 78:
        fout.write("https://www.blockchain.com" + a + '\n')
fout.close()
