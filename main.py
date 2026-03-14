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


def pergunta_1(bd):
    """Pergunta 1: Qual o percentual de jogos gratuitos e pagos na plataforma?"""
    resultado = bd.percentual_gratuitos_pagos()

    print("\n" + "=" * 60)
    print("PERGUNTA 1: Qual o percentual de jogos gratuitos e pagos na")
    print("plataforma?")
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

    print("\n--- Análise ---")
    print(
        "Dos 72.934 jogos cadastrados na Steam, 60.254 (82,61%) são pagos "
        "e 12.680 (17,39%) são gratuitos. Ou seja, a cada 5 jogos na "
        "plataforma, aproximadamente 4 são pagos e 1 é gratuito. Esse "
        "número faz sentido quando pensamos que a Steam funciona, antes de "
        "tudo, como uma loja digital, então é esperado que a maioria dos "
        "títulos tenha um preço definido. Ainda assim, quase 13 mil jogos "
        "gratuitos é um número expressivo. Boa parte desses títulos segue "
        "o modelo free-to-play, em que o jogo em si é gratuito, mas o "
        "jogador pode gastar dinheiro com itens cosméticos, passes de "
        "temporada ou conteúdo adicional. Jogos como Dota 2, "
        "Counter-Strike 2 e Apex Legends são exemplos conhecidos desse "
        "modelo. Do ponto de vista da Fun Corp., entender essa divisão é "
        "importante para decidir se vale mais a pena lançar um jogo pago "
        "com preço fixo ou apostar no modelo gratuito com microtransações."
    )


def pergunta_2(bd):
    """Pergunta 2: Qual o ano com o maior número de novos jogos?"""
    resultado = bd.ano_com_mais_lancamentos()

    print("\n" + "=" * 60)
    print("PERGUNTA 2: Qual o ano com o maior número de novos jogos?")
    print("Em caso de empate, retorne uma lista com os anos empatados.")
    print("=" * 60)

    if len(resultado["anos"]) == 1:
        print(f"\nO ano com mais lançamentos foi: {resultado['anos'][0]}")
    else:
        print(f"\nAnos empatados: {resultado['anos']}")

    print(f"Quantidade de novos jogos: {resultado['quantidade']}")

    print("\nDistribuição completa por ano:")
    print(f"{'Ano':<8} {'Jogos':>8}  Barra")
    print("-" * 50)

    qtd_maxima = max(resultado["contagem_por_ano"].values())
    for ano, qtd in sorted(resultado["contagem_por_ano"].items()):
        barra = "#" * int(qtd / qtd_maxima * 30)
        print(f"{ano:<8} {qtd:>8}  {barra}")

    print("\n--- Análise ---")
    print(
        "O ano de 2022 foi o que teve mais jogos novos publicados na Steam: "
        "13.951 títulos. Olhando a tabela de distribuição por ano, dá para "
        "perceber que o número de lançamentos cresceu muito a partir de "
        "2014. Naquele ano foram 1.584 jogos; em 2022, quase 14 mil, algo "
        "em torno de 9 vezes mais. Uma das razões para esse crescimento é "
        "que ficou mais fácil desenvolver e publicar jogos ao longo dos "
        "anos. Motores como Unity e Unreal Engine se tornaram gratuitos "
        "para projetos menores, e em 2017 a Valve substituiu o antigo "
        "Steam Greenlight pelo Steam Direct, que simplificou bastante o "
        "processo de publicação na plataforma. O valor de 2023 aparece "
        "baixo (4.908 jogos), mas isso acontece porque os dados foram "
        "coletados em maio de 2023, ou seja, o ano ainda não tinha "
        "terminado. Também chama atenção o registro de 1 jogo em 2025, "
        "que provavelmente se trata de um erro no cadastro ou de um jogo "
        "com data de lançamento futura já registrada. Para a Fun Corp., "
        "esses números mostram que o mercado de jogos digitais está em "
        "expansão, mas também que a concorrência por visibilidade na "
        "plataforma é cada vez maior."
    )


def pergunta_3(bd):
    """Pergunta 3 (própria): Quais gêneros possuem a melhor recepção?"""
    resultado = bd.generos_por_aprovacao(minimo_jogos=50)

    print("\n" + "=" * 65)
    print("PERGUNTA 3: Para demonstrar a facilidade de revisão e")
    print("modificação de uso do módulo desenvolvido, uma pergunta")
    print("adicional deve ser proposta e respondida por você.")
    print("")
    print("Pergunta proposta: Quais gêneros de jogos possuem a melhor")
    print("recepção pela comunidade, considerando o percentual médio de")
    print("avaliações positivas? (Mínimo de 50 jogos com avaliações)")
    print("=" * 65)
    print(f"\n{'Pos':<5} {'Gênero':<25} {'Total':<8} {'Avaliados':<12} Aprovação")
    print("-" * 65)

    for i, item in enumerate(resultado, 1):
        barra = "#" * int(item["media_aprovacao"] / 100 * 20)
        print(
            f"{i:<5} {item['genero']:<25} {item['total_jogos']:<8} "
            f"{item['jogos_com_avaliacoes']:<12} "
            f"{item['media_aprovacao']:.2f}% {barra}"
        )

    print("\n--- Análise ---")
    print(
        "O ranking mostra que os gêneros Casual (75,22%), Indie (75,11%) "
        "e Adventure (74,72%) têm as maiores médias de aprovação entre os "
        "jogos da Steam, considerando apenas gêneros com pelo menos 50 "
        "jogos avaliados. Já os gêneros com pior recepção são Violent "
        "(58,56%) e Gore (59,37%), o que pode indicar que jogos com foco "
        "apenas em violência, sem outros atrativos, tendem a ser mal "
        "avaliados pelos jogadores. Vale observar que Casual e Indie "
        "também são os gêneros com mais jogos no catálogo (29.362 e "
        "49.568 respectivamente), o que dá mais confiança na média "
        "calculada. Entre os gêneros com mais de 1.000 jogos avaliados, "
        "o pior colocado é Massively Multiplayer com 63,44%. Isso pode "
        "estar relacionado ao fato de que jogos online massivos dependem "
        "de servidores estáveis e de uma base de jogadores ativa, e "
        "quando isso não acontece, as avaliações negativas aumentam. "
        "Para a Fun Corp., os dados indicam que gêneros como Casual, "
        "Indie e Adventure oferecem uma boa combinação de volume de "
        "mercado e boa recepção do público, o que os torna opções "
        "interessantes para uma empresa que está começando no mercado "
        "digital."
    )


def pergunta_1_amostra(bd_amostra):
    """Pergunta 1 sobre a amostra: Percentual de jogos gratuitos e pagos."""
    resultado = bd_amostra.percentual_gratuitos_pagos()

    print("\n" + "=" * 60)
    print("PERGUNTA 1 (AMOSTRA): Qual o percentual de jogos gratuitos e")
    print("pagos na plataforma?")
    print("=" * 60)
    print(f"\nTotal de jogos na amostra: {resultado['total']}")
    print(
        f"\nJogos GRATUITOS: {resultado['gratuitos']:>6} "
        f"({resultado['percentual_gratuitos']:.2f}%)"
    )
    print(
        f"Jogos PAGOS:     {resultado['pagos']:>6} "
        f"({resultado['percentual_pagos']:.2f}%)"
    )

    print("\n--- Análise ---")
    print(
        "Na amostra de 20 jogos, 4 são gratuitos (20,00%) e 16 são pagos "
        "(80,00%). O resultado bate com o que foi calculado manualmente. "
        "A proporção ficou bem próxima do dataset completo (17,39% "
        "gratuitos e 82,61% pagos), o que mostra que a amostra conseguiu "
        "manter uma distribuição parecida com a do arquivo original. Isso "
        "também serve para validar que o método "
        "percentual_gratuitos_pagos() está funcionando corretamente, já "
        "que o valor retornado pelo programa é o mesmo que obtivemos ao "
        "contar na mão."
    )


def pergunta_2_amostra(bd_amostra):
    """Pergunta 2 sobre a amostra: Ano com maior número de novos jogos."""
    resultado = bd_amostra.ano_com_mais_lancamentos()

    print("\n" + "=" * 60)
    print("PERGUNTA 2 (AMOSTRA): Qual o ano com o maior número de novos")
    print("jogos? Em caso de empate, retorne uma lista com os anos")
    print("empatados.")
    print("=" * 60)

    if len(resultado["anos"]) == 1:
        print(f"\nO ano com mais lançamentos foi: {resultado['anos'][0]}")
    else:
        print(f"\nAnos empatados: {resultado['anos']}")

    print(f"Quantidade de novos jogos: {resultado['quantidade']}")
    print(f"Contagem por ano: {resultado['contagem_por_ano']}")

    print("\n--- Análise ---")
    print(
        "O ano com mais lançamentos na amostra foi 2022, com 5 jogos. O "
        "resultado confere com o cálculo manual. A contagem por ano ficou "
        "assim: 2015 (1), 2016 (1), 2017 (1), 2019 (4), 2020 (2), "
        "2021 (4), 2022 (5) e 2023 (2). Os anos de 2019 e 2021 ficaram "
        "empatados com 4 jogos cada, logo atrás de 2022. Essa "
        "concentração nos anos mais recentes faz sentido, pois no dataset "
        "completo também se observa um aumento forte no número de "
        "lançamentos a partir de 2018. Não houve empate no primeiro "
        "lugar, mas o método está preparado para retornar uma lista caso "
        "isso aconteça. O resultado confirma que o método "
        "ano_com_mais_lancamentos() funciona de acordo com o esperado."
    )


def pergunta_3_amostra(bd_amostra):
    """Pergunta 3 sobre a amostra: Gêneros por percentual de aprovação."""
    resultado = bd_amostra.generos_por_aprovacao()

    print("\n" + "=" * 65)
    print("PERGUNTA 3 (AMOSTRA): Para demonstrar a facilidade de revisão")
    print("e modificação de uso do módulo desenvolvido, uma pergunta")
    print("adicional deve ser proposta e respondida por você.")
    print("")
    print("Pergunta proposta: Quais gêneros de jogos possuem a melhor")
    print("recepção pela comunidade? (Sem filtro de mínimo)")
    print("=" * 65)
    print(f"\n{'Pos':<5} {'Gênero':<25} {'Total':<8} {'Avaliados':<12} Aprovação")
    print("-" * 65)

    for i, item in enumerate(resultado, 1):
        print(
            f"{i:<5} {item['genero']:<25} {item['total_jogos']:<8} "
            f"{item['jogos_com_avaliacoes']:<12} {item['media_aprovacao']:.2f}%"
        )

    print("\n--- Análise ---")
    print(
        "Na amostra, o gênero Racing aparece em primeiro lugar com 100% "
        "de aprovação, mas tem apenas 1 jogo avaliado, então esse valor "
        "não é muito confiável. Os gêneros com mais jogos avaliados na "
        "amostra são Indie (13 jogos, 88,66% de aprovação) e Action (9 "
        "jogos, 91,74%). Esses dois gêneros também apareceram bem "
        "posicionados no dataset completo, o que mostra consistência nos "
        "resultados. Na parte de baixo do ranking, Game Development, "
        "Utilities e Design & Illustration tiveram apenas 9,09% de "
        "aprovação cada, mas novamente com apenas 1 jogo cada, então não "
        "dá para tirar conclusões definitivas. O valor do Indie (15 jogos "
        "no total, 13 com avaliações, média de 88,66%) confere exatamente "
        "com o cálculo feito manualmente, o que valida o funcionamento do "
        "método generos_por_aprovacao(). As médias na amostra são mais "
        "altas do que no dataset completo (por exemplo, Indie com 88,66% "
        "na amostra contra 75,11% no completo), o que é esperado em uma "
        "amostra pequena, onde poucos jogos muito bem avaliados podem "
        "puxar a média para cima."
    )


def principal():
    """Função principal que executa todo o fluxo da Fase 1."""
    # 1. Executa os testes automatizados.
    testes_ok = executar_testes()

    if not testes_ok:
        print("\nOs testes falharam. Corrija os erros antes de prosseguir.")
        return

    # ============================================================
    # PARTE 1: Respostas sobre o conjunto de dados COMPLETO
    # ============================================================
    print("\n" + "=" * 60)
    print("RESPOSTAS SOBRE O CONJUNTO DE DADOS COMPLETO")
    print("=" * 60)

    bd = BaseDeDados("./steam_games.csv")
    print(f"Total de jogos carregados: {bd.total_jogos}")

    pergunta_1(bd)
    pergunta_2(bd)
    pergunta_3(bd)

    # ============================================================
    # PARTE 2: Respostas sobre a AMOSTRA de 20 jogos
    # ============================================================
    print("\n" + "=" * 60)
    print("RESPOSTAS SOBRE A AMOSTRA DE 20 JOGOS")
    print("(Resultados conferidos com cálculos manuais)")
    print("=" * 60)

    bd_amostra = BaseDeDados("data/amostra_20_jogos.csv")
    print(f"Jogos na amostra: {bd_amostra.total_jogos}")

    pergunta_1_amostra(bd_amostra)
    pergunta_2_amostra(bd_amostra)
    pergunta_3_amostra(bd_amostra)

    print("\n" + "=" * 60)
    print("FIM DA ANÁLISE - FASE 1")
    print("=" * 60)


if __name__ == "__main__":
    principal()
