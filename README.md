# Fase 1 - Projeto Final: Programação para Dados

## Análise Exploratória de Dados da Plataforma Steam

A Fun Corp., uma empresa de jogos em ascensão, deseja expandir suas operações para o mercado de jogos digitais. Para montar uma estratégia de expansão, realizou uma coleta de dados na Steam, uma das maiores plataformas de distribuição de jogos digitais do mundo.

Este projeto utiliza a biblioteca `analisejogossteam`, desenvolvida como um módulo reutilizável em Python com orientação a objetos, para carregar e consultar os dados coletados. O programa responde a três perguntas:

1. Qual o percentual de jogos gratuitos e pagos na plataforma?
2. Qual o ano com o maior número de novos jogos?
3. Quais gêneros possuem a melhor recepção pela comunidade? (Pergunta própria, cruzando gêneros com avaliações positivas/negativas.)

## Estrutura do Projeto

```
analisejogossteam/
├── analisejogossteam/                     # Biblioteca principal (módulo reutilizável)
│   ├── __init__.py                        # Exporta as classes públicas
│   ├── modelos.py                         # Classe Jogo (modelo de dados)
│   ├── banco_de_dados.py                  # Classe BaseDeDados (carga e consultas)
│   └── excecoes.py                        # Exceções customizadas
├── data/
│   ├── amostra_20_jogos.csv               # Amostra de 20 jogos aleatórios para testes
│   └── formulas_validacao.txt             # Fórmulas do LibreOffice Calc para validação manual
├── tests/
│   ├── __init__.py
│   └── test_analisejogossteam.py          # Testes automatizados (20 testes)
├── Fase 1 - Projeto Final: Programação para Dados.ipynb  # Notebook Jupyter com as respostas
├── gerar_amostra.py                       # Script que gerou a amostra aleatória
├── main.py                                # Programa principal com as respostas
├── .gitignore
└── README.md
```

## Pré-requisitos

- Python 3.8 ou superior.
- O arquivo `steam_games.csv` deve estar na raiz do projeto.
- Este projeto utiliza apenas bibliotecas da biblioteca padrão do Python (`csv`, `os`, `collections`, `unittest`, `random`, `sys`), portanto não há dependências externas a serem instaladas.

## Como executar o programa

1. Certifique-se de que o arquivo `steam_games.csv` está na raiz do projeto:

```
analisejogossteam/
├── steam_games.csv
├── main.py
└── ...
```

2. Execute o programa principal:

```bash
python3 main.py
```

O programa irá:
- Executar os 20 testes automatizados sobre a amostra de 20 jogos.
- Verificar que os resultados da amostra conferem com os cálculos manuais.
- Carregar o dataset completo (72.934 jogos).
- Exibir as respostas e análises das três perguntas.

## Como executar apenas os testes

```bash
python3 -m unittest tests.test_analisejogossteam -v
```

Os testes verificam os resultados sobre a amostra de 20 jogos, cujos valores esperados foram calculados manualmente para garantir a corretude do sistema.

## Como regenerar a amostra

A amostra de 20 jogos já está incluída em `data/amostra_20_jogos.csv`. Caso deseje regenerá-la (a semente aleatória é fixa, portanto o resultado será idêntico):

```bash
python3 gerar_amostra.py
```

## Como utilizar a biblioteca `analisejogossteam`

A biblioteca pode ser importada e utilizada por qualquer outro programa Python:

```python
from analisejogossteam import BaseDeDados

bd = BaseDeDados("caminho/para/steam_games.csv")

# Pergunta 1: percentual de jogos gratuitos e pagos.
print(bd.percentual_gratuitos_pagos())

# Pergunta 2: ano com mais lançamentos.
print(bd.ano_com_mais_lancamentos())

# Pergunta 3: gêneros por aprovação (mínimo de 50 jogos avaliados).
print(bd.generos_por_aprovacao(minimo_jogos=50))

# Acessar a lista de jogos diretamente.
for jogo in bd.jogos[:5]:
    print(jogo.nome, jogo.preco, jogo.generos)
```
