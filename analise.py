import os
import time
import json
from random import random
from datetime import datetime
import requests
import pandas as pd
import seaborn as sns
from sys import argv

if len(argv) < 2:
    print("Uso: python analise.py <nome-do-grafico>")
    exit(1)

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

# ======== PARTE 1: EXTRAÇÃO ========
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

print("Extração concluída.")

# ======== PARTE 2: VISUALIZAÇÃO ========
df = pd.read_csv('taxa-cdi.csv')
grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
_ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
grafico.get_figure().savefig(f"{argv[1]}.png")

print(f"Análise completa! Gráfico salvo como {argv[1]}.png")
