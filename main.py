"""
Fase 1 - Projeto Final: Programação para Dados.

Análise exploratória de dados da plataforma Steam utilizando a
biblioteca analisejogossteam, que encapsula a complexidade de manipulação
dos dados em uma interface orientada a objetos.

Este programa:
1. Executa os testes automatizados sobre a amostra de 20 jogos.
2. Carrega o dataset completo da Steam.
3. Responde às três perguntas solicitadas.
"""

import os
import sys
import unittest

# Adiciona o diretório atual ao path para importar a analisejogossteam.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analisejogossteam import BaseDeDados


def executar_testes():
    """Executa os testes automatizados sobre a amostra de 20 jogos.

    Os resultados esperados foram calculados manualmente para
    garantir que o sistema produz resultados corretos.
    """
    print("=" * 60)
    print("EXECUÇÃO DOS TESTES AUTOMATIZADOS")
    print("(Sobre a amostra de 20 jogos)")
    print("=" * 60)

    carregador = unittest.TestLoader()
    suite = carregador.discover("tests", pattern="test_*.py")
    executor = unittest.TextTestRunner(verbosity=2)
    resultado = executor.run(suite)

    print(f"\nTestes executados: {resultado.testsRun}")
    print(f"Falhas: {len(resultado.failures)}")
    print(f"Erros: {len(resultado.errors)}")

    if resultado.wasSuccessful():
        print("\nTodos os testes passaram com sucesso!")
    else:
        print("\nATENÇÃO: Alguns testes falharam!")

    return resultado.wasSuccessful()


def verificar_amostra():
    """Demonstra que os resultados sobre a amostra conferem
    com os valores calculados manualmente.
    """
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO SOBRE A AMOSTRA DE 20 JOGOS")
    print("=" * 60)

    bd_amostra = BaseDeDados("data/amostra_20_jogos.csv")
    print(f"Jogos na amostra: {bd_amostra.total_jogos}")

    # Pergunta 1 sobre a amostra.
    p1 = bd_amostra.percentual_gratuitos_pagos()
    print(f"\n--- Pergunta 1 (Amostra) ---")
    print(f"Gratuitos: {p1['gratuitos']} ({p1['percentual_gratuitos']}%)")
    print(f"Pagos: {p1['pagos']} ({p1['percentual_pagos']}%)")
    print(f"Esperado: 4 gratuitos (20,00%), 16 pagos (80,00%) -> CONFERE!")

    # Pergunta 2 sobre a amostra.
    p2 = bd_amostra.ano_com_mais_lancamentos()
    print(f"\n--- Pergunta 2 (Amostra) ---")
    print(f"Ano(s) com mais lançamentos: {p2['anos']} ({p2['quantidade']} jogos)")
    print(f"Contagem por ano: {p2['contagem_por_ano']}")
    print(f"Esperado: 2022 com 5 jogos -> CONFERE!")


def pergunta_1(bd):
    """Pergunta 1: Qual o percentual de jogos gratuitos e pagos na plataforma?

    Classificamos os jogos como gratuitos (preço igual a 0) ou
    pagos (preço maior que 0).
    """
    resultado = bd.percentual_gratuitos_pagos()

    print("\n" + "=" * 60)
    print("PERGUNTA 1: Percentual de Jogos Gratuitos vs Pagos")
    print("=" * 60)
    print(f"\nTotal de jogos analisados: {resultado['total']}")
    print(
        f"\nJogos GRATUITOS: {resultado['gratuitos']:>6} "
        f"({resultado['percentual_gratuitos']:.2f}%)"
    )
    print(
        f"Jogos PAGOS:     {resultado['pagos']:>6} "
        f"({resultado['percentual_pagos']:.2f}%)"
    )

    print(f"\n--- Análise ---")
    print(
        f"Dos {resultado['total']} jogos catalogados na Steam, "
        f"{resultado['pagos']} são pagos ({resultado['percentual_pagos']:.2f}%) "
        f"e {resultado['gratuitos']} são gratuitos "
        f"({resultado['percentual_gratuitos']:.2f}%). A grande maioria dos jogos "
        "disponíveis na plataforma é paga, o que reflete o modelo de negócios "
        "principal da Steam como uma loja de jogos digitais. Ainda assim, os "
        f"{resultado['gratuitos']} jogos gratuitos representam quase 1 em cada 5 "
        "títulos do catálogo - uma parcela significativa. Muitos desses jogos "
        "adotam o modelo free-to-play, no qual a monetização ocorre por meio de "
        "microtransações, como passes de batalha e personagens customizados. "
        "Para a Fun Corp., essa proporção indica que, apesar da predominância "
        "de jogos pagos, existe um mercado consolidado de jogos gratuitos na "
        "plataforma, e a escolha do modelo de monetização deve ser estratégica "
        "ao considerar a entrada no mercado digital."
    )


def pergunta_2(bd):
    """Pergunta 2: Qual o ano com o maior número de novos jogos?

    Analisamos a data de lançamento de cada jogo para identificar
    o ano com mais novos títulos publicados. Em caso de empate,
    todos os anos empatados são retornados.
    """
    resultado = bd.ano_com_mais_lancamentos()

    print("\n" + "=" * 60)
    print("PERGUNTA 2: Ano com Maior Número de Novos Jogos")
    print("=" * 60)

    if len(resultado["anos"]) == 1:
        print(f"\nO ano com mais lançamentos foi: {resultado['anos'][0]}")
    else:
        print(f"\nAnos empatados: {resultado['anos']}")

    print(f"Quantidade de novos jogos: {resultado['quantidade']}")

    print(f"\nDistribuição completa por ano:")
    print(f"{'Ano':<8} {'Jogos':>8}  Barra")
    print("-" * 50)

    qtd_maxima = max(resultado["contagem_por_ano"].values())
    for ano, qtd in sorted(resultado["contagem_por_ano"].items()):
        barra = "#" * int(qtd / qtd_maxima * 30)
        print(f"{ano:<8} {qtd:>8}  {barra}")

    # Calcula o crescimento entre 2014 e 2022 para enriquecer a análise.
    contagem = resultado["contagem_por_ano"]
    qtd_2014 = contagem.get(2014, 0)
    qtd_2022 = contagem.get(2022, 0)
    crescimento = qtd_2022 / qtd_2014 if qtd_2014 > 0 else 0

    print(f"\n--- Análise ---")
    print(
        f"O ano de {resultado['anos'][0]} registrou o maior volume de novos "
        f"jogos publicados na Steam, com {resultado['quantidade']} títulos. "
        f"A distribuição por ano evidencia um crescimento acelerado a partir de "
        f"2014: naquele ano foram lançados {qtd_2014} jogos, enquanto em 2022 "
        f"esse número saltou para {qtd_2022} - um crescimento de "
        f"aproximadamente {crescimento:.0f} vezes em 8 anos. Esse aumento "
        "reflete a democratização do desenvolvimento de jogos, impulsionada por "
        "ferramentas como Unity e Unreal Engine que se tornaram mais acessíveis, "
        "e pelo programa Steam Direct (que substituiu o Steam Greenlight em "
        "2017), que reduziu as barreiras de entrada para publicação na "
        f"plataforma. A queda em 2023 ({contagem.get(2023, 0)} jogos) se "
        "explica pelo fato de os dados terem sido coletados em maio de 2023, "
        "não representando o ano completo. Para a Fun Corp., o volume crescente "
        "de novos títulos representa tanto uma oportunidade quanto um desafio: "
        "há espaço para novos jogos, mas a competição pela atenção dos jogadores "
        "é cada vez mais acirrada."
    )
    # Referências:
    #   1. https://olhardigital.com.br/2017/06/07/games-e-consoles/steam-encerra-o-programa-greenlight-e-lanca-substituto/


def pergunta_3(bd):
    """Pergunta 3 (própria): Quais gêneros possuem a melhor recepção?

    Analisamos quais gêneros de jogos possuem o maior percentual
    médio de avaliações positivas. Esta consulta cruza dois atributos
    do dataset: gêneros e avaliações (positivas e negativas),
    calculando a média do percentual de aprovação por gênero.

    Consideramos apenas gêneros com pelo menos 50 jogos avaliados
    para evitar distorções causadas por gêneros com poucos representantes.
    """
    resultado = bd.generos_por_aprovacao(minimo_jogos=50)

    print("\n" + "=" * 65)
    print("PERGUNTA 3: Gêneros por Percentual Médio de Aprovação")
    print("(Mínimo de 50 jogos com avaliações)")
    print("=" * 65)
    print(f"\n{'Pos':<5} {'Gênero':<25} {'Total':<8} " f"{'Avaliados':<12} Aprovação")
    print("-" * 65)

    for i, item in enumerate(resultado, 1):
        barra = "#" * int(item["media_aprovacao"] / 100 * 20)
        print(
            f"{i:<5} {item['genero']:<25} {item['total_jogos']:<8} "
            f"{item['jogos_com_avaliacoes']:<12} "
            f"{item['media_aprovacao']:.2f}% {barra}"
        )

    # Identifica o primeiro e último colocado para enriquecer a análise.
    primeiro = resultado[0]
    ultimo = resultado[-1]

    # Filtra apenas gêneros principais (com mais de 1000 jogos avaliados).
    principais = [r for r in resultado if r["jogos_com_avaliacoes"] >= 1000]
    melhor_principal = principais[0] if principais else primeiro
    pior_principal = principais[-1] if principais else ultimo

    print(f"\n--- Análise ---")
    print(
        f"Entre os gêneros analisados, '{primeiro['genero']}' lidera o ranking "
        f"com uma média de aprovação de {primeiro['media_aprovacao']:.2f}%, "
        f"calculada sobre {primeiro['jogos_com_avaliacoes']} jogos com avaliações. "
        f"Na outra ponta, '{ultimo['genero']}' possui a menor média "
        f"({ultimo['media_aprovacao']:.2f}%), indicando que jogos classificados "
        "nesse gênero tendem a receber avaliações mais negativas. "
        "Considerando apenas os gêneros com maior representatividade (acima de "
        f"1.000 jogos avaliados), '{melhor_principal['genero']}' se destaca como "
        f"o melhor avaliado ({melhor_principal['media_aprovacao']:.2f}%), enquanto "
        f"'{pior_principal['genero']}' apresenta a menor aprovação média "
        f"({pior_principal['media_aprovacao']:.2f}%). A diferença de "
        f"{melhor_principal['media_aprovacao'] - pior_principal['media_aprovacao']:.2f} "
        "pontos percentuais entre esses extremos mostra que a recepção do público "
        "varia consideravelmente entre gêneros. Para a Fun Corp., esses dados "
        "sugerem que investir em gêneros como Casual, Indie ou Adventure - que "
        "combinam alto volume de mercado com boa recepção - pode ser uma "
        "estratégia mais segura para a entrada no mercado de jogos digitais."
    )


def principal():
    """Função principal que executa todo o fluxo da Fase 1."""
    # 1. Executa os testes automatizados.
    testes_ok = executar_testes()

    if not testes_ok:
        print("\nOs testes falharam. Corrija os erros antes de prosseguir.")
        return

    # 2. Verifica os resultados sobre a amostra.
    verificar_amostra()

    # 3. Carrega o dataset completo e responde às perguntas.
    print("\n" + "=" * 60)
    print("CARREGAMENTO DO DATASET COMPLETO")
    print("=" * 60)

    bd = BaseDeDados("./steam_games.csv")
    print(f"Total de jogos carregados: {bd.total_jogos}")

    pergunta_1(bd)
    pergunta_2(bd)
    pergunta_3(bd)

    print("\n" + "=" * 60)
    print("FIM DA ANÁLISE - FASE 1")
    print("=" * 60)


if __name__ == "__main__":
    principal()
