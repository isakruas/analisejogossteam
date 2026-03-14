"""
Módulo principal da analisejogossteam para carregamento e consulta de dados.

Fornece a classe BaseDeDados, que encapsula toda a lógica de
leitura do CSV e execução de consultas sobre os dados de jogos.
"""

import csv
import os
from collections import Counter, defaultdict

from analisejogossteam.excecoes import (
    ArquivoNaoEncontradoErro,
    ConsultaInvalidaErro,
    DadosInvalidosErro,
)
from analisejogossteam.modelos import Jogo


class BaseDeDados:
    """Classe principal para carregar e consultar dados de jogos da Steam.

    Carrega um arquivo CSV com dados de jogos e disponibiliza métodos
    para realizar consultas e análises sobre os dados.

    Exemplo:
        >>> bd = BaseDeDados("steam_games.csv")
        >>> resultado = bd.percentual_gratuitos_pagos()
        >>> print(resultado)
    """

    def __init__(self, caminho_csv):
        """Inicializa o banco de dados carregando o arquivo CSV.

        Args:
            caminho_csv (str): Caminho para o arquivo CSV.

        Lança:
            ArquivoNaoEncontradoErro: Se o arquivo não existir.
            DadosInvalidosErro: Se o arquivo estiver vazio ou corrompido.
        """
        if not os.path.exists(caminho_csv):
            raise ArquivoNaoEncontradoErro(caminho_csv)

        self._jogos = []
        self._carregar(caminho_csv)

        if not self._jogos:
            raise DadosInvalidosErro("O arquivo CSV não contém dados de jogos.")

    def _carregar(self, caminho_csv):
        """Carrega os jogos a partir do arquivo CSV.

        Args:
            caminho_csv (str): Caminho para o arquivo CSV.

        Lança:
            DadosInvalidosErro: Se ocorrer erro ao ler o arquivo.
        """
        try:
            with open(caminho_csv, encoding="utf-8") as arquivo:
                leitor = csv.DictReader(arquivo)
                for linha in leitor:
                    jogo = Jogo(linha)
                    self._jogos.append(jogo)
        except csv.Error as e:
            raise DadosInvalidosErro(f"Erro ao processar o CSV: {e}")

    @property
    def jogos(self):
        """Retorna a lista de todos os jogos carregados.

        Retorna:
            list[Jogo]: Lista de objetos Jogo.
        """
        return list(self._jogos)

    @property
    def total_jogos(self):
        """Retorna o número total de jogos no banco de dados.

        Retorna:
            int: Total de jogos.
        """
        return len(self._jogos)

    # ----- Pergunta 1 -----

    def percentual_gratuitos_pagos(self):
        """Calcula o percentual de jogos gratuitos e pagos na plataforma.

        Retorna:
            dict: Dicionário com as chaves 'gratuitos', 'pagos',
                  'percentual_gratuitos' e 'percentual_pagos'.

        Lança:
            DadosInvalidosErro: Se não houver jogos carregados.
        """
        total = self.total_jogos
        if total == 0:
            raise DadosInvalidosErro("Nenhum jogo disponível para análise.")

        gratuitos = sum(1 for jogo in self._jogos if jogo.eh_gratuito)
        pagos = total - gratuitos

        return {
            "gratuitos": gratuitos,
            "pagos": pagos,
            "total": total,
            "percentual_gratuitos": round(gratuitos / total * 100, 2),
            "percentual_pagos": round(pagos / total * 100, 2),
        }

    # ----- Pergunta 2 -----

    def ano_com_mais_lancamentos(self):
        """Identifica o ano com o maior número de novos jogos lançados.

        Em caso de empate, retorna uma lista com todos os anos empatados.

        Retorna:
            dict: Dicionário com as chaves 'anos' (lista de anos),
                  'quantidade' (número de jogos) e 'contagem_por_ano'
                  (dicionário completo de contagens).

        Lança:
            DadosInvalidosErro: Se nenhum jogo possuir data de lançamento.
        """
        contagem = Counter()
        for jogo in self._jogos:
            ano = jogo.ano_lancamento
            if ano is not None:
                contagem[ano] += 1

        if not contagem:
            raise DadosInvalidosErro("Nenhum jogo possui data de lançamento válida.")

        max_quantidade = max(contagem.values())
        anos_empatados = sorted(
            [ano for ano, qtd in contagem.items() if qtd == max_quantidade]
        )

        return {
            "anos": anos_empatados,
            "quantidade": max_quantidade,
            "contagem_por_ano": dict(sorted(contagem.items())),
        }

    # ----- Pergunta 3 (própria) -----

    def generos_por_aprovacao(self, minimo_jogos=1):
        """Analisa os gêneros de jogos ordenados pelo percentual médio
        de avaliações positivas, considerando apenas gêneros que possuam
        pelo menos 'minimo_jogos' com avaliações.

        Esta consulta cruza dois atributos (gêneros e avaliações positivas/
        negativas) para identificar quais gêneros possuem a melhor recepção
        pela comunidade.

        Args:
            minimo_jogos (int): Número mínimo de jogos com avaliações para
                                o gênero ser incluído. Padrão: 1.

        Retorna:
            list[dict]: Lista de dicionários ordenada por percentual médio
                        de aprovação (decrescente), contendo:
                        - 'genero': nome do gênero
                        - 'total_jogos': total de jogos no gênero
                        - 'jogos_com_avaliacoes': jogos que possuem avaliações
                        - 'media_aprovacao': percentual médio de aprovação

        Lança:
            ConsultaInvalidaErro: Se minimo_jogos for menor que 1.
        """
        if minimo_jogos < 1:
            raise ConsultaInvalidaErro(
                "O parâmetro minimo_jogos deve ser pelo menos 1."
            )

        genero_total = Counter()
        genero_aprovacoes = defaultdict(list)

        for jogo in self._jogos:
            for genero in jogo.generos:
                genero_total[genero] += 1
                percentual = jogo.percentual_positivas
                if percentual is not None:
                    genero_aprovacoes[genero].append(percentual)

        resultado = []
        for genero, total in genero_total.items():
            aprovacoes = genero_aprovacoes[genero]
            if len(aprovacoes) >= minimo_jogos:
                media = sum(aprovacoes) / len(aprovacoes)
                resultado.append(
                    {
                        "genero": genero,
                        "total_jogos": total,
                        "jogos_com_avaliacoes": len(aprovacoes),
                        "media_aprovacao": round(media, 2),
                    }
                )

        resultado.sort(key=lambda x: x["media_aprovacao"], reverse=True)
        return resultado
