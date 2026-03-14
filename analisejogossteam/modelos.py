"""
Módulo de modelos de dados da analisejogossteam.

Define a classe Jogo, que representa um jogo da plataforma Steam
com todos os seus atributos.
"""


class Jogo:
    """Representa um jogo da plataforma Steam.

    Atributos:
        id_aplicativo (int): Identificador único do jogo.
        nome (str): Nome do jogo.
        data_lancamento (str): Data de lançamento no formato original.
        proprietarios_estimados (str): Faixa estimada de proprietários.
        pico_usuarios_simultaneos (int): Pico de usuários simultâneos.
        idade_minima (int): Idade mínima requerida.
        preco (float): Preço do jogo em dólares.
        quantidade_dlc (int): Número de DLCs.
        descricao (str): Descrição do jogo.
        idiomas (str): Idiomas suportados.
        idiomas_audio (str): Idiomas de áudio completos.
        avaliacoes (str): Texto de avaliações.
        windows (bool): Compatível com Windows.
        mac (bool): Compatível com Mac.
        linux (bool): Compatível com Linux.
        nota_metacritic (int): Nota no Metacritic.
        nota_usuario (int): Nota dos usuários.
        positivas (int): Número de avaliações positivas.
        negativas (int): Número de avaliações negativas.
        conquistas (int): Número de conquistas.
        recomendacoes (int): Número de recomendações.
        tempo_medio (int): Tempo médio de jogo (minutos).
        tempo_mediano (int): Tempo mediano de jogo (minutos).
        desenvolvedores (str): Desenvolvedores do jogo.
        editoras (str): Editoras do jogo.
        categorias (list): Lista de categorias.
        generos (list): Lista de gêneros.
        etiquetas (list): Lista de etiquetas (tags).
    """

    def __init__(self, dicionario_dados):
        """Inicializa um Jogo a partir de um dicionário (linha do CSV).

        Args:
            dicionario_dados (dict): Dicionário com os campos do CSV.
        """
        self.id_aplicativo = self._para_inteiro(dicionario_dados.get("AppID", "0"))
        self.nome = dicionario_dados.get("Name", "").strip()
        self.data_lancamento = dicionario_dados.get("Release date", "").strip()
        self.proprietarios_estimados = dicionario_dados.get(
            "Estimated owners", ""
        ).strip()
        self.pico_usuarios_simultaneos = self._para_inteiro(
            dicionario_dados.get("Peak CCU", "0")
        )
        self.idade_minima = self._para_inteiro(
            dicionario_dados.get("Required age", "0")
        )
        self.preco = self._para_decimal(dicionario_dados.get("Price", "0"))
        self.quantidade_dlc = self._para_inteiro(dicionario_dados.get("DLC count", "0"))
        self.descricao = dicionario_dados.get("About the game", "")
        self.idiomas = dicionario_dados.get("Supported languages", "")
        self.idiomas_audio = dicionario_dados.get("Full audio languages", "")
        self.avaliacoes = dicionario_dados.get("Reviews", "")
        self.windows = self._para_booleano(dicionario_dados.get("Windows", "False"))
        self.mac = self._para_booleano(dicionario_dados.get("Mac", "False"))
        self.linux = self._para_booleano(dicionario_dados.get("Linux", "False"))
        self.nota_metacritic = self._para_inteiro(
            dicionario_dados.get("Metacritic score", "0")
        )
        self.nota_usuario = self._para_inteiro(dicionario_dados.get("User score", "0"))
        self.positivas = self._para_inteiro(dicionario_dados.get("Positive", "0"))
        self.negativas = self._para_inteiro(dicionario_dados.get("Negative", "0"))
        self.conquistas = self._para_inteiro(dicionario_dados.get("Achievements", "0"))
        self.recomendacoes = self._para_inteiro(
            dicionario_dados.get("Recommendations", "0")
        )
        self.tempo_medio = self._para_inteiro(
            dicionario_dados.get("Average playtime forever", "0")
        )
        self.tempo_mediano = self._para_inteiro(
            dicionario_dados.get("Median playtime forever", "0")
        )
        self.desenvolvedores = dicionario_dados.get("Developers", "").strip()
        self.editoras = dicionario_dados.get("Publishers", "").strip()
        self.categorias = self._para_lista(dicionario_dados.get("Categories", ""))
        self.generos = self._para_lista(dicionario_dados.get("Genres", ""))
        self.etiquetas = self._para_lista(dicionario_dados.get("Tags", ""))

    @staticmethod
    def _para_inteiro(valor):
        """Converte um valor para inteiro, retornando 0 se inválido."""
        try:
            return int(valor)
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def _para_decimal(valor):
        """Converte um valor para decimal, retornando 0.0 se inválido."""
        try:
            return float(valor)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _para_booleano(valor):
        """Converte um valor para booleano."""
        return str(valor).strip().lower() in ("true", "1", "yes")

    @staticmethod
    def _para_lista(valor):
        """Converte uma string separada por vírgulas em lista."""
        if not valor or not valor.strip():
            return []
        return [item.strip() for item in valor.split(",") if item.strip()]

    @property
    def eh_gratuito(self):
        """Retorna True se o jogo é gratuito (preço == 0)."""
        return self.preco == 0.0

    @property
    def ano_lancamento(self):
        """Extrai o ano de lançamento a partir da data.

        Retorna:
            int ou None: Ano de lançamento, ou None se não disponível.
        """
        if not self.data_lancamento:
            return None
        partes = self.data_lancamento.split(", ")
        if len(partes) == 2:
            try:
                return int(partes[1])
            except ValueError:
                return None
        # Tenta interpretar como apenas o ano.
        try:
            return int(self.data_lancamento.strip())
        except ValueError:
            return None

    @property
    def percentual_positivas(self):
        """Calcula o percentual de avaliações positivas.

        Retorna:
            float ou None: Percentual de avaliações positivas,
                           ou None se não houver avaliações.
        """
        total = self.positivas + self.negativas
        if total == 0:
            return None
        return (self.positivas / total) * 100

    def __repr__(self):
        return (
            f"Jogo(id_aplicativo={self.id_aplicativo}, "
            f"nome='{self.nome}', preco={self.preco})"
        )

    def __str__(self):
        tipo = "Gratuito" if self.eh_gratuito else f"US$ {self.preco:.2f}"
        return f"{self.nome} ({tipo})"
