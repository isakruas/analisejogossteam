"""
Módulo de exceções customizadas da analisejogossteam.

Define exceções específicas para tratamento de erros durante
o carregamento e consulta dos dados da Steam.
"""


class AnaliseJogosSteamErro(Exception):
    """Exceção base para todos os erros da analisejogossteam."""

    pass


class ArquivoNaoEncontradoErro(AnaliseJogosSteamErro):
    """Exceção lançada quando o arquivo CSV não é encontrado."""

    def __init__(self, caminho):
        self.caminho = caminho
        super().__init__(f"Arquivo não encontrado: {caminho}")


class DadosInvalidosErro(AnaliseJogosSteamErro):
    """Exceção lançada quando os dados do CSV estão em formato inválido."""

    def __init__(self, mensagem="Dados inválidos no arquivo CSV."):
        super().__init__(mensagem)


class ConsultaInvalidaErro(AnaliseJogosSteamErro):
    """Exceção lançada quando uma consulta recebe parâmetros inválidos."""

    def __init__(self, mensagem="Parâmetros de consulta inválidos."):
        super().__init__(mensagem)
