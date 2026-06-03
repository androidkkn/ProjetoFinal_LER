"""Módulo de validação de entradas do usuário."""


class Validadores:
    """Funções utilitárias para validação de dados de entrada."""

    @staticmethod
    def validar_nota(valor: float) -> bool:
        """Valida se uma nota está no intervalo permitido (0.0 a 10.0).

        Args:
            valor: Valor da nota a ser validado.

        Returns:
            True se a nota é válida, False caso contrário.
        """
        return 0.0 <= valor <= 10.0

    @staticmethod
    def validar_frequencia(aulas_assistidas: int, aulas_total: int) -> bool:
        """Valida os dados de frequência.

        Args:
            aulas_assistidas: Número de aulas assistidas.
            aulas_total: Total de aulas.

        Returns:
            True se os dados são válidos, False caso contrário.
        """
        if aulas_total <= 0:
            return False
        if aulas_assistidas < 0:
            return False
        if aulas_assistidas > aulas_total:
            return False
        return True

    @staticmethod
    def validar_matricula(matricula: str) -> bool:
        """Valida se a matrícula não está vazia e contém apenas
        caracteres alfanuméricos.

        Args:
            matricula: String da matrícula a validar.

        Returns:
            True se a matrícula é válida, False caso contrário.
        """
        return bool(matricula) and matricula.strip().isalnum()

    @staticmethod
    def validar_nome(nome: str) -> bool:
        """Valida se o nome não está vazio e tem pelo menos 2 caracteres.

        Args:
            nome: Nome a validar.

        Returns:
            True se o nome é válido, False caso contrário.
        """
        return bool(nome) and len(nome.strip()) >= 2

    @staticmethod
    def ler_float(mensagem: str, minimo: float = 0.0, maximo: float = 10.0) -> float:
        """Lê um valor float do terminal com validação.

        Args:
            mensagem: Mensagem exibida ao usuário.
            minimo: Valor mínimo aceito.
            maximo: Valor máximo aceito.

        Returns:
            O valor float validado.
        """
        while True:
            try:
                valor = float(input(mensagem))
                if minimo <= valor <= maximo:
                    return valor
                print(f"  ❌ Valor deve estar entre {minimo} e {maximo}.")
            except ValueError:
                print("  ❌ Entrada inválida. Digite um número.")

    @staticmethod
    def ler_int(mensagem: str, minimo: int = 0, maximo: int = 999) -> int:
        """Lê um valor inteiro do terminal com validação.

        Args:
            mensagem: Mensagem exibida ao usuário.
            minimo: Valor mínimo aceito.
            maximo: Valor máximo aceito.

        Returns:
            O valor inteiro validado.
        """
        while True:
            try:
                valor = int(input(mensagem))
                if minimo <= valor <= maximo:
                    return valor
                print(f"  ❌ Valor deve estar entre {minimo} e {maximo}.")
            except ValueError:
                print("  ❌ Entrada inválida. Digite um número inteiro.")

    @staticmethod
    def ler_string(mensagem: str, minimo: int = 1) -> str:
        """Lê uma string do terminal com validação de tamanho mínimo.

        Args:
            mensagem: Mensagem exibida ao usuário.
            minimo: Tamanho mínimo da string.

        Returns:
            A string validada (sem espaços extras).
        """
        while True:
            valor = input(mensagem).strip()
            if len(valor) >= minimo:
                return valor
            print(f"  ❌ Entrada deve ter pelo menos {minimo} caractere(s).")
