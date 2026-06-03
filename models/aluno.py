"""Modelo de dados para Aluno."""

from dataclasses import dataclass, field
from typing import Optional

from models.disciplina import Disciplina


@dataclass
class Aluno:
    """Representa um aluno matriculado no sistema.

    Attributes:
        matricula: Código identificador único do aluno.
        nome: Nome completo do aluno.
        disciplinas: Lista de disciplinas em que o aluno está matriculado.
    """

    matricula: str
    nome: str
    disciplinas: list[Disciplina] = field(default_factory=list)

    # ── Métodos de gerenciamento de disciplinas ──────────────────────

    def adicionar_disciplina(self, disciplina: Disciplina) -> None:
        """Adiciona uma disciplina ao aluno.

        Args:
            disciplina: A disciplina a ser adicionada.

        Raises:
            ValueError: Se o aluno já está matriculado na disciplina.
        """
        if self.buscar_disciplina(disciplina.nome) is not None:
            raise ValueError(
                f"Aluno '{self.nome}' já está matriculado em '{disciplina.nome}'."
            )
        self.disciplinas.append(disciplina)

    def buscar_disciplina(self, nome_disciplina: str) -> Optional[Disciplina]:
        """Busca uma disciplina pelo nome.

        Args:
            nome_disciplina: Nome da disciplina a ser buscada.

        Returns:
            A disciplina encontrada ou None.
        """
        for disciplina in self.disciplinas:
            if disciplina.nome.lower() == nome_disciplina.lower():
                return disciplina
        return None

    # ── Serialização ─────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Converte o aluno em dicionário para serialização JSON."""
        return {
            "matricula": self.matricula,
            "nome": self.nome,
            "disciplinas": [d.to_dict() for d in self.disciplinas],
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Aluno":
        """Cria uma instância de Aluno a partir de um dicionário.

        Args:
            dados: Dicionário com os dados do aluno.

        Returns:
            Instância de Aluno reconstruída.
        """
        aluno = cls(
            matricula=dados["matricula"],
            nome=dados["nome"],
        )
        for disc_dados in dados.get("disciplinas", []):
            aluno.disciplinas.append(Disciplina.from_dict(disc_dados))
        return aluno

    def __str__(self) -> str:
        return f"[{self.matricula}] {self.nome} — {len(self.disciplinas)} disciplina(s)"
