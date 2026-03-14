"""
analisejogossteam - Biblioteca para análise de dados da plataforma Steam.

Esta biblioteca oferece uma interface orientada a objetos para carregar,
consultar e analisar dados de jogos da plataforma Steam a partir de
arquivos CSV.

Exemplo de uso:
    >>> from analisejogossteam import BaseDeDados
    >>> bd = BaseDeDados("caminho/para/steam_games.csv")
    >>> print(bd.percentual_gratuitos_pagos())
    >>> print(bd.ano_com_mais_lancamentos())
"""

from analisejogossteam.banco_de_dados import BaseDeDados
from analisejogossteam.excecoes import (
    ArquivoNaoEncontradoErro,
    ConsultaInvalidaErro,
    DadosInvalidosErro,
)
from analisejogossteam.modelos import Jogo

__all__ = [
    "Jogo",
    "BaseDeDados",
    "ArquivoNaoEncontradoErro",
    "DadosInvalidosErro",
    "ConsultaInvalidaErro",
]
