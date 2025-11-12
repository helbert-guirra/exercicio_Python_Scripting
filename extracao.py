import os
import time
import json
from random import random
from datetime import datetime
import requests

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

try:
    response = requests.get(url=URL)
    response.raise_for_status()
except requests.HTTPError:
    print("Dado não encontrado, continuando.")
    dado = None
except Exception as exc:
    print("Erro, parando a execução.")
    raise exc
else:
    dado = json.loads(response.text)[-1]['valor']

for _ in range(10):
    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')
    cdi = float(dado) + (random() - 0.5)

    if not os.path.exists('taxa-cdi.csv'):
        with open('taxa-cdi.csv', 'w', encoding='utf8') as f:
            f.write('data,hora,taxa\n')

    with open('taxa-cdi.csv', 'a', encoding='utf8') as f:
        f.write(f'{data},{hora},{cdi}\n')

    time.sleep(1)

print("Sucesso - arquivo taxa-cdi.csv criado!")
