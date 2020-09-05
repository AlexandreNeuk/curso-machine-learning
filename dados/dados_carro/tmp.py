import pandas as pd
import requests as rq
import bs4 as bs4
import time
from random import randint

print('Ini')
df = pd.read_json("tmp.json", lines=True)
df.head(10).sort_values("title")

def icarros_save_page(page, i):
    with open('./Carro-{}.html'.format(i), 'w+', encoding='utf-8') as f:
        f.write(page)
		
tmp = []
i = 125
url_icarros = 'https://www.icarros.com.br'
for index, row in df.iterrows():
    urll = url_icarros + row['link']
    if i % 2 == 0:
        value = randint(22, 38)
    else:
        value = randint(33, 41)
            
    response = rq.get(urll)
    icarros_save_page(response.text, i)
    print('value ', value, ' -- ', urll)
    time.sleep(value)
    i = i + 1

print('Fim')

