"""Serviço de persistência de dados em formato JSON."""

import json
import os
from typing import Optional

from models.aluno import Aluno


class Persistencia:
    """Gerencia o salvamento e carregamento de dados de alunos em JSON.

    Attributes:
        caminho_arquivo: Caminho do arquivo JSON de dados.
    """

    def __init__(self, caminho_arquivo: str = "dados/alunos.json"):
        """Inicializa o serviço de persistência.

        Args:
            caminho_arquivo: Caminho para o arquivo JSON.
        """
        self.caminho_arquivo = caminho_arquivo

    def _garantir_diretorio(self) -> None:
        """Cria o diretório de dados se não existir."""
        diretorio = os.path.dirname(self.caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)

    def salvar(self, alunos: list[Aluno]) -> None:
        """Salva a lista de alunos no arquivo JSON.

        Args:
            alunos: Lista de alunos a ser salva.
        """
        self._garantir_diretorio()
        dados = {"alunos": [aluno.to_dict() for aluno in alunos]}

        with open(self.caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    def carregar(self) -> list[Aluno]:
        """Carrega a lista de alunos do arquivo JSON.

        Returns:
            Lista de alunos carregados. Lista vazia se o arquivo
            não existir.
        """
        if not os.path.exists(self.caminho_arquivo):
            return []

        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            alunos = []
            for aluno_dados in dados.get("alunos", []):
                alunos.append(Aluno.from_dict(aluno_dados))
            return alunos

        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️  Erro ao carregar dados: {e}")
            print("    Iniciando com lista vazia.")
            return []

    def buscar_aluno(
        self, alunos: list[Aluno], matricula: str
    ) -> Optional[Aluno]:
        """Busca um aluno pela matrícula.

        Args:
            alunos: Lista de alunos onde buscar.
            matricula: Matrícula do aluno a buscar.

        Returns:
            O aluno encontrado ou None.
        """
        for aluno in alunos:
            if aluno.matricula == matricula:
                return aluno
        return None
