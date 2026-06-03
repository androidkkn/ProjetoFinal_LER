"""Modelo de dados para Disciplina."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Disciplina:
    """Representa uma disciplina cursada por um aluno.

    Attributes:
        nome: Nome da disciplina.
        notas: Lista com até 3 notas (N1, N2, N3), valores entre 0.0 e 10.0.
        aulas_total: Total de aulas ministradas na disciplina.
        aulas_assistidas: Número de aulas que o aluno compareceu.
    """

    nome: str
    notas: list[float] = field(default_factory=list)
    aulas_total: int = 0
    aulas_assistidas: int = 0

    # ── Propriedades calculadas ──────────────────────────────────────

    @property
    def media(self) -> Optional[float]:
        """Calcula a média aritmética das notas.

        Returns:
            A média das notas ou None se não houver notas registradas.
        """
        if not self.notas:
            return None
        return sum(self.notas) / len(self.notas)

    @property
    def frequencia(self) -> Optional[float]:
        """Calcula o percentual de frequência do aluno.

        Returns:
            Percentual de frequência (0.0 a 100.0) ou None se
            o total de aulas for zero.
        """
        if self.aulas_total == 0:
            return None
        return (self.aulas_assistidas / self.aulas_total) * 100

    @property
    def notas_completas(self) -> bool:
        """Verifica se as 3 notas foram registradas."""
        return len(self.notas) == 3

    # ── Serialização ─────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Converte a disciplina em dicionário para serialização JSON."""
        return {
            "nome": self.nome,
            "notas": self.notas,
            "aulas_total": self.aulas_total,
            "aulas_assistidas": self.aulas_assistidas,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Disciplina":
        """Cria uma instância de Disciplina a partir de um dicionário.

        Args:
            dados: Dicionário com os dados da disciplina.

        Returns:
            Instância de Disciplina reconstruída.
        """
        return cls(
            nome=dados["nome"],
            notas=dados.get("notas", []),
            aulas_total=dados.get("aulas_total", 0),
            aulas_assistidas=dados.get("aulas_assistidas", 0),
        )

    def __str__(self) -> str:
        media_str = f"{self.media:.2f}" if self.media is not None else "N/A"
        freq_str = f"{self.frequencia:.1f}%" if self.frequencia is not None else "N/A"
        return f"{self.nome} | Média: {media_str} | Frequência: {freq_str}"
