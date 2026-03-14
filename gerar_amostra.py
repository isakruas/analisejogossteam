"""
Script para gerar a amostra de 20 jogos aleatórios do dataset.

A amostra é selecionada aleatoriamente (não os 20 primeiros jogos,
conforme orientação do enunciado). Executar uma única vez para gerar
o arquivo data/amostra_20_jogos.csv.
"""

import csv
import random

random.seed(42)  # Semente fixa para reprodutibilidade.

CAMINHO_DATASET = "./steam_games.csv"
CAMINHO_AMOSTRA = "data/amostra_20_jogos.csv"

with open(CAMINHO_DATASET, encoding="utf-8") as f:
    leitor = csv.reader(f)
    cabecalho = next(leitor)
    todas_linhas = list(leitor)

# Exclui os 20 primeiros jogos, conforme orientação do enunciado.
linhas_disponiveis = todas_linhas[20:]

amostra = random.sample(linhas_disponiveis, 20)

with open(CAMINHO_AMOSTRA, "w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    escritor.writerow(cabecalho)
    escritor.writerows(amostra)

print(f"Amostra de {len(amostra)} jogos salva em {CAMINHO_AMOSTRA}")
