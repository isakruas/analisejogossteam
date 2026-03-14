"""
Testes automatizados para a biblioteca analisejogossteam.

Os testes são executados sobre a amostra de 20 jogos
(data/amostra_20_jogos.csv) e os resultados esperados foram
calculados manualmente para garantir a corretude do sistema.

Resultados esperados (amostra de 20 jogos):
- Pergunta 1: 4 gratuitos (20,00%), 16 pagos (80,00%).
- Pergunta 2: Ano 2022 com 5 lançamentos.
- Pergunta 3: O gênero 'Casual' possui a maior média de aprovação
              entre os gêneros com pelo menos 5 jogos avaliados.
"""

import os
import sys
import unittest

# Adiciona o diretório pai ao path para importar a analisejogossteam.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analisejogossteam import (
    ArquivoNaoEncontradoErro,
    BaseDeDados,
    ConsultaInvalidaErro,
    DadosInvalidosErro,
)
from analisejogossteam.modelos import Jogo

# Caminho da amostra de 20 jogos.
CAMINHO_AMOSTRA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "amostra_20_jogos.csv",
)


class TesteJogo(unittest.TestCase):
    """Testes para a classe Jogo."""

    def teste_jogo_gratuito(self):
        """Testa se um jogo com preço 0 é identificado como gratuito."""
        dados = {"Price": "0", "Name": "Jogo Grátis"}
        jogo = Jogo(dados)
        self.assertTrue(jogo.eh_gratuito)

    def teste_jogo_pago(self):
        """Testa se um jogo com preço > 0 é identificado como pago."""
        dados = {"Price": "9.99", "Name": "Jogo Pago"}
        jogo = Jogo(dados)
        self.assertFalse(jogo.eh_gratuito)

    def teste_ano_lancamento(self):
        """Testa a extração do ano de lançamento."""
        dados = {"Release date": "Oct 21, 2008"}
        jogo = Jogo(dados)
        self.assertEqual(jogo.ano_lancamento, 2008)

    def teste_ano_lancamento_apenas_ano(self):
        """Testa a extração quando só o ano está disponível."""
        dados = {"Release date": "2020"}
        jogo = Jogo(dados)
        self.assertEqual(jogo.ano_lancamento, 2020)

    def teste_ano_lancamento_vazio(self):
        """Testa retorno None quando a data de lançamento está vazia."""
        dados = {"Release date": ""}
        jogo = Jogo(dados)
        self.assertIsNone(jogo.ano_lancamento)

    def teste_percentual_positivas(self):
        """Testa o cálculo do percentual de avaliações positivas."""
        dados = {"Positive": "80", "Negative": "20"}
        jogo = Jogo(dados)
        self.assertAlmostEqual(jogo.percentual_positivas, 80.0)

    def teste_percentual_positivas_sem_avaliacoes(self):
        """Testa retorno None quando não há avaliações."""
        dados = {"Positive": "0", "Negative": "0"}
        jogo = Jogo(dados)
        self.assertIsNone(jogo.percentual_positivas)

    def teste_generos_lista(self):
        """Testa a conversão de gêneros para lista."""
        dados = {"Genres": "Action,Adventure,Indie"}
        jogo = Jogo(dados)
        self.assertEqual(jogo.generos, ["Action", "Adventure", "Indie"])

    def teste_generos_vazio(self):
        """Testa lista vazia quando não há gêneros."""
        dados = {"Genres": ""}
        jogo = Jogo(dados)
        self.assertEqual(jogo.generos, [])


class TesteBaseDeDadosExcecoes(unittest.TestCase):
    """Testes de exceções da classe BaseDeDados."""

    def teste_arquivo_inexistente(self):
        """Testa exceção ao tentar carregar arquivo inexistente."""
        with self.assertRaises(ArquivoNaoEncontradoErro):
            BaseDeDados("arquivo_que_nao_existe.csv")


class TesteBaseDeDadosAmostra(unittest.TestCase):
    """Testes sobre a amostra de 20 jogos.

    Os resultados esperados foram calculados manualmente
    para verificar a corretude do sistema.
    """

    @classmethod
    def setUpClass(cls):
        """Carrega a amostra uma única vez para todos os testes."""
        cls.bd = BaseDeDados(CAMINHO_AMOSTRA)

    def teste_total_jogos_amostra(self):
        """Verifica que a amostra contém exatamente 20 jogos."""
        self.assertEqual(self.bd.total_jogos, 20)

    # --- Testes da Pergunta 1 ---

    def teste_percentual_gratuitos(self):
        """Verifica: 4 jogos gratuitos = 20,00% (calculado manualmente)."""
        resultado = self.bd.percentual_gratuitos_pagos()
        self.assertEqual(resultado["gratuitos"], 4)
        self.assertAlmostEqual(resultado["percentual_gratuitos"], 20.00)

    def teste_percentual_pagos(self):
        """Verifica: 16 jogos pagos = 80,00% (calculado manualmente)."""
        resultado = self.bd.percentual_gratuitos_pagos()
        self.assertEqual(resultado["pagos"], 16)
        self.assertAlmostEqual(resultado["percentual_pagos"], 80.00)

    def teste_soma_percentuais_100(self):
        """Verifica que a soma dos percentuais é 100%."""
        resultado = self.bd.percentual_gratuitos_pagos()
        soma = resultado["percentual_gratuitos"] + resultado["percentual_pagos"]
        self.assertAlmostEqual(soma, 100.0)

    # --- Testes da Pergunta 2 ---

    def teste_ano_mais_lancamentos(self):
        """Verifica: ano 2022 com 5 lançamentos (calculado manualmente)."""
        resultado = self.bd.ano_com_mais_lancamentos()
        self.assertEqual(resultado["anos"], [2022])
        self.assertEqual(resultado["quantidade"], 5)

    def teste_contagem_anos_completa(self):
        """Verifica a contagem completa por ano (calculada manualmente)."""
        resultado = self.bd.ano_com_mais_lancamentos()
        contagem = resultado["contagem_por_ano"]
        esperado = {
            2015: 1,
            2016: 1,
            2017: 1,
            2019: 4,
            2020: 2,
            2021: 4,
            2022: 5,
            2023: 2,
        }
        self.assertEqual(contagem, esperado)

    # --- Testes da Pergunta 3 ---

    def teste_generos_por_aprovacao_retorna_lista(self):
        """Verifica que o retorno é uma lista não vazia."""
        resultado = self.bd.generos_por_aprovacao()
        self.assertIsInstance(resultado, list)
        self.assertGreater(len(resultado), 0)

    def teste_generos_por_aprovacao_ordenado(self):
        """Verifica que os resultados estão ordenados por aprovação decrescente."""
        resultado = self.bd.generos_por_aprovacao()
        medias = [r["media_aprovacao"] for r in resultado]
        self.assertEqual(medias, sorted(medias, reverse=True))

    def teste_generos_por_aprovacao_indie(self):
        """Verifica dados do gênero Indie (calculados manualmente).

        Indie: 13 jogos com avaliações, média de aprovação ~ 88,66%.
        """
        resultado = self.bd.generos_por_aprovacao()
        indie = next(r for r in resultado if r["genero"] == "Indie")
        self.assertEqual(indie["total_jogos"], 15)
        self.assertEqual(indie["jogos_com_avaliacoes"], 13)
        self.assertAlmostEqual(indie["media_aprovacao"], 88.66, places=1)

    def teste_generos_por_aprovacao_minimo_invalido(self):
        """Verifica exceção com parâmetro minimo_jogos inválido."""
        with self.assertRaises(ConsultaInvalidaErro):
            self.bd.generos_por_aprovacao(minimo_jogos=0)


if __name__ == "__main__":
    unittest.main()
