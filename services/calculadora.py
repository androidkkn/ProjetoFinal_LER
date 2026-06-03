"""Serviço de cálculo de médias e determinação de status do aluno."""

from models.disciplina import Disciplina


class Status:
    """Constantes para os status possíveis do aluno."""

    APROVADO = "APROVADO"
    RECUPERACAO = "RECUPERAÇÃO"
    REPROVADO_DIRETO = "REPROVADO DIRETO"
    REPROVADO_FALTA = "REPROVADO POR FALTA"
    INCOMPLETO = "DADOS INCOMPLETOS"


class Calculadora:
    """Serviço responsável pelo cálculo de médias e status do aluno.

    Implementa todas as regras de negócio de aprovação:
    - Média >= 7.0 e Frequência >= 75% → Aprovado
    - Média >= 5.0 e < 7.0 e Frequência >= 75% → Recuperação
    - Média < 5.0 → Reprovado Direto
    - Frequência < 75% (qualquer média) → Reprovado por Falta
    """

    MEDIA_APROVACAO = 7.0
    MEDIA_RECUPERACAO = 5.0
    FREQUENCIA_MINIMA = 75.0

    @staticmethod
    def calcular_media(notas: list[float]) -> float:
        """Calcula a média aritmética de uma lista de notas.

        Args:
            notas: Lista de notas numéricas.

        Returns:
            A média aritmética das notas.

        Raises:
            ValueError: Se a lista de notas estiver vazia.
        """
        if not notas:
            raise ValueError("A lista de notas não pode estar vazia.")
        return sum(notas) / len(notas)

    @staticmethod
    def calcular_frequencia(aulas_assistidas: int, aulas_total: int) -> float:
        """Calcula o percentual de frequência.

        Args:
            aulas_assistidas: Número de aulas que o aluno compareceu.
            aulas_total: Total de aulas ministradas.

        Returns:
            Percentual de frequência (0.0 a 100.0).

        Raises:
            ValueError: Se o total de aulas for zero ou negativo.
        """
        if aulas_total <= 0:
            raise ValueError("O total de aulas deve ser maior que zero.")
        if aulas_assistidas < 0:
            raise ValueError("Aulas assistidas não pode ser negativo.")
        if aulas_assistidas > aulas_total:
            raise ValueError(
                "Aulas assistidas não pode exceder o total de aulas."
            )
        return (aulas_assistidas / aulas_total) * 100

    @classmethod
    def determinar_status(cls, disciplina: Disciplina) -> str:
        """Determina o status do aluno em uma disciplina.

        A frequência é verificada ANTES da média (RN05).

        Args:
            disciplina: A disciplina a ser avaliada.

        Returns:
            String com o status do aluno (APROVADO, RECUPERAÇÃO,
            REPROVADO DIRETO, REPROVADO POR FALTA ou DADOS INCOMPLETOS).
        """
        # Verificar se há dados suficientes
        if disciplina.media is None or disciplina.frequencia is None:
            return Status.INCOMPLETO

        if not disciplina.notas_completas:
            return Status.INCOMPLETO

        frequencia = disciplina.frequencia
        media = disciplina.media

        # RN05: A frequência é verificada antes da média
        if frequencia < cls.FREQUENCIA_MINIMA:
            return Status.REPROVADO_FALTA

        # RN02: Lógica de aprovação por média
        if media >= cls.MEDIA_APROVACAO:
            return Status.APROVADO
        elif media >= cls.MEDIA_RECUPERACAO:
            return Status.RECUPERACAO
        else:
            return Status.REPROVADO_DIRETO
