"""Serviço de geração de boletim final do aluno."""

from models.aluno import Aluno
from services.calculadora import Calculadora


class GeradorBoletim:
    """Gera o boletim escolar final formatado para exibição no terminal."""

    # Larguras das colunas
    _COL_DISC = 16
    _COL_NOTA = 6
    _COL_MEDIA = 7
    _COL_FREQ = 8
    _COL_STATUS = 10

    @classmethod
    def gerar(cls, aluno: Aluno) -> str:
        """Gera o boletim final completo de um aluno.

        Args:
            aluno: O aluno cujo boletim será gerado.

        Returns:
            String formatada com o boletim completo.
        """
        largura = 68
        linhas: list[str] = []

        # ── Cabeçalho ────────────────────────────────────────────────
        linhas.append("╔" + "═" * largura + "╗")
        linhas.append("║" + "BOLETIM ESCOLAR".center(largura) + "║")
        linhas.append("╠" + "═" * largura + "╣")
        linhas.append("║" + f"  Aluno: {aluno.nome}".ljust(largura) + "║")
        linhas.append("║" + f"  Matrícula: {aluno.matricula}".ljust(largura) + "║")
        linhas.append("╠" + "═" * largura + "╣")

        # ── Cabeçalho da tabela ──────────────────────────────────────
        cabecalho = (
            f"  {'Disciplina':<{cls._COL_DISC}}"
            f"│ {'N1':^{cls._COL_NOTA}}"
            f"│ {'N2':^{cls._COL_NOTA}}"
            f"│ {'N3':^{cls._COL_NOTA}}"
            f"│ {'Média':^{cls._COL_MEDIA}}"
            f"│ {'Freq.':^{cls._COL_FREQ}}"
            f"│ {'Status':^{cls._COL_STATUS}}"
        )
        linhas.append("║" + cabecalho.ljust(largura) + "║")

        separador = (
            f"  {'─' * cls._COL_DISC}"
            f"┼{'─' * (cls._COL_NOTA + 1)}"
            f"┼{'─' * (cls._COL_NOTA + 1)}"
            f"┼{'─' * (cls._COL_NOTA + 1)}"
            f"┼{'─' * (cls._COL_MEDIA + 1)}"
            f"┼{'─' * (cls._COL_FREQ + 1)}"
            f"┼{'─' * (cls._COL_STATUS + 1)}"
        )
        linhas.append("║" + separador.ljust(largura) + "║")

        # ── Dados das disciplinas ────────────────────────────────────
        if not aluno.disciplinas:
            linhas.append("║" + "  Nenhuma disciplina cadastrada.".ljust(largura) + "║")
        else:
            for disc in aluno.disciplinas:
                status = Calculadora.determinar_status(disc)
                status_abrev = cls._abreviar_status(status)

                # Formatar notas
                n1 = f"{disc.notas[0]:.1f}" if len(disc.notas) > 0 else "---"
                n2 = f"{disc.notas[1]:.1f}" if len(disc.notas) > 1 else "---"
                n3 = f"{disc.notas[2]:.1f}" if len(disc.notas) > 2 else "---"

                media_str = f"{disc.media:.2f}" if disc.media is not None else "---"
                freq_str = f"{disc.frequencia:.1f}%" if disc.frequencia is not None else "---"

                nome_disc = disc.nome[:cls._COL_DISC]

                linha = (
                    f"  {nome_disc:<{cls._COL_DISC}}"
                    f"│ {n1:^{cls._COL_NOTA}}"
                    f"│ {n2:^{cls._COL_NOTA}}"
                    f"│ {n3:^{cls._COL_NOTA}}"
                    f"│ {media_str:^{cls._COL_MEDIA}}"
                    f"│ {freq_str:^{cls._COL_FREQ}}"
                    f"│ {status_abrev:^{cls._COL_STATUS}}"
                )
                linhas.append("║" + linha.ljust(largura) + "║")

        # ── Rodapé ───────────────────────────────────────────────────
        linhas.append("╠" + "═" * largura + "╣")

        # Legenda
        linhas.append("║" + "  Legenda:".ljust(largura) + "║")
        linhas.append("║" + "    APROV. = Aprovado  │  RECUP. = Recuperação".ljust(largura) + "║")
        linhas.append("║" + "    REPROV. = Reprovado Direto  │  R.FALTA = Reprovado por Falta".ljust(largura) + "║")
        linhas.append("║" + "  ".ljust(largura) + "║")

        # Resumo
        resumo = cls._gerar_resumo(aluno)
        for linha_resumo in resumo:
            linhas.append("║" + f"  {linha_resumo}".ljust(largura) + "║")

        linhas.append("╚" + "═" * largura + "╝")

        return "\n".join(linhas)

    @classmethod
    def _gerar_resumo(cls, aluno: Aluno) -> list[str]:
        """Gera as linhas de resumo do boletim.

        Args:
            aluno: O aluno para gerar o resumo.

        Returns:
            Lista de strings com o resumo.
        """
        total = len(aluno.disciplinas)
        if total == 0:
            return ["Sem disciplinas para resumir."]

        contagem = {"APROVADO": 0, "RECUPERAÇÃO": 0, "REPROVADO": 0, "INCOMPLETO": 0}
        for disc in aluno.disciplinas:
            status = Calculadora.determinar_status(disc)
            if status == "APROVADO":
                contagem["APROVADO"] += 1
            elif status == "RECUPERAÇÃO":
                contagem["RECUPERAÇÃO"] += 1
            elif status == "DADOS INCOMPLETOS":
                contagem["INCOMPLETO"] += 1
            else:
                contagem["REPROVADO"] += 1

        linhas = [
            f"Resumo: {total} disciplina(s) cursada(s)",
            f"  ✅ Aprovado: {contagem['APROVADO']}",
            f"  ⚠️  Recuperação: {contagem['RECUPERAÇÃO']}",
            f"  ❌ Reprovado: {contagem['REPROVADO']}",
        ]
        if contagem["INCOMPLETO"] > 0:
            linhas.append(f"  ⬜ Incompleto: {contagem['INCOMPLETO']}")

        return linhas

    @staticmethod
    def _abreviar_status(status: str) -> str:
        """Abrevia o status para caber na coluna do boletim.

        Args:
            status: Status completo.

        Returns:
            Status abreviado.
        """
        abreviacoes = {
            "APROVADO": "APROV.",
            "RECUPERAÇÃO": "RECUP.",
            "REPROVADO DIRETO": "REPROV.",
            "REPROVADO POR FALTA": "R.FALTA",
            "DADOS INCOMPLETOS": "INCOMP.",
        }
        return abreviacoes.get(status, status)
