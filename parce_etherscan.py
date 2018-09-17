from requests import get
from bs4 import BeautifulSoup


fout = open('ether.txt', 'w')
count = 0
for i in range(6190000, 6195001):
    j = 1
    url = 'https://etherscan.io/txs?block=' + str(i) + '&pr=' + str(j)
    soup = BeautifulSoup(get(url).text, "html.parser")
    number = int(soup.find_all(attrs={
        'id':"spinwheel", 
        'class':"fa fa-spin fa-spinner fa-2x fa-pulse", 
        'style':"display: none; margin-top: 4px"
        })[0].parent.text[14:-20])
    content = soup.body.div.find_all(attrs={
        'id':"ContentPlaceHolder1_mainrow", 
        'class':'row'})[0].div.div.table.tbody.find_all('tr')  
    for k in range(number // 50 + (number % 50 != 0)):
        for link in content:
            c = link.contents
            if c[5].span:
                contract = int(bool(c[5].span.i))
                a = [
                    c[0].text, c[2].span.get('title'), c[3].text, 
                    c[5].text, c[6].text, c[7].text, str(contract)
                ]
                tx = '\n#\n'.join(a) + '\n\n\n'
                fout.write(tx)
            else:
                contract = c[5].a.get('title')
                a = [
                    c[0].text, c[2].span.get('title'), c[3].text, 
                    contract, c[6].text, c[7].text, 'creation'
                ]
                tx = '\n#\n'.join(a) + '\n\n\n'
            count += 1
        j += 1
        url = 'https://etherscan.io/txs?block=' + str(i) + '&pr=' + str(j)
        soup = BeautifulSoup(get(url).text, "html.parser")
        content = soup.body.div.find_all(attrs={
            'id':"ContentPlaceHolder1_mainrow", 
            'class':'row'})[0].div.div.table.tbody.find_all('tr')          
fout.close()    