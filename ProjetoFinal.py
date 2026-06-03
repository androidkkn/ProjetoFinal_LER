"""
EduGrade — Sistema de Gestão de Notas Escolares
================================================
Ponto de entrada principal do sistema.
Gerencia o menu interativo e as operações do usuário.
"""

import os  # Biblioteca padrão do Python para interagir com caminhos e sistema de arquivos
import sys # Biblioteca padrão para controle do interpretador e encerramento de programas

# MÓDULOS INTERNOS DO PROJETO:
# ----------------------------
# Importam as classes e serviços criados para estruturar a aplicação seguindo boas práticas de divisão de responsabilidades.
from models.aluno import Aluno
from models.disciplina import Disciplina
from services.calculadora import Calculadora
from services.boletim import GeradorBoletim
from services.persistencia import Persistencia
from utils.validadores import Validadores


class EduGrade:
    """Classe principal do sistema EduGrade.

    Gerencia a interação com o usuário através de um menu no terminal.
    """

    def __init__(self):
        """Inicializa o sistema EduGrade."""
        # CAMINHO DO ARQUIVO DE DADOS:
        # 1. os.path.abspath(__file__) descobre o caminho completo deste script (antiGTest.py)
        # 2. os.path.dirname(...) pega a pasta em que este arquivo está contido
        # 3. os.path.join(...) concatena a pasta com a subpasta "dados" e o arquivo "alunos.json"
        # Isso garante que o caminho seja gerado de forma dinâmica e não estática, funcionando em qualquer máquina.
        caminho_dados = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "dados",
            "alunos.json",
        )
        
        # self.persistencia: Instancia o serviço de gravação/leitura de arquivos JSON.
        self.persistencia = Persistencia(caminho_arquivo=caminho_dados)
        
        # self.alunos: Carrega a lista de alunos cadastrados a partir do arquivo JSON.
        # Se o arquivo não existir ou estiver corrompido, a persistência retornará uma lista vazia.
        self.alunos: list[Aluno] = self.persistencia.carregar()
        
        # self.validadores: Instancia a classe utilitária de validação de entradas de teclado.
        self.validadores = Validadores()

    # ── Menu Principal ───────────────────────────────────────────────

    def exibir_menu(self) -> None:
        """Exibe o menu principal do sistema desenhado em caracteres ASCII/Unicode."""
        print()
        print("══════════════════════════════════════════")
        print("         📚 EduGrade                      ")
        print("   Gestão de Notas Escolares              ")
        print("══════════════════════════════════════════")
        print("  1. Cadastrar Aluno                      ")
        print("  2. Cadastrar Disciplina para Aluno      ")
        print("  3. Registrar Notas                      ")
        print("  4. Registrar Frequência                 ")
        print("  5. Gerar Boletim do Aluno               ")
        print("  6. Listar Todos os Alunos               ")
        print("  7. Consultar Status por Disciplina      ")
        print("  8. Remover Disciplina de Aluno          ")
        print("  9. Remover Aluno (Matrícula)            ")
        print("  0. Sair                                 ")
        print("══════════════════════════════════════════")

    def executar(self) -> None:
        """Loop principal de execução do sistema.
        
        Exibe o menu repetidamente e direciona a escolha do usuário para a função correta.
        """
        print("\n🎓 Bem-vindo ao EduGrade — Sistema de Gestão de Notas Escolares!")

        while True:
            # Exibe o menu visual
            self.exibir_menu()
            
            # .strip() remove espaços extras antes e depois da opção digitada
            opcao = input("\n  Escolha uma opção: ").strip()

            # DICIONÁRIO DE AÇÕES (Padrão Dispatcher):
            # Mapeia cada caractere de opção diretamente para a referência do método da classe.
            # Evita o uso excessivo de blocos 'if-elif-else'.
            acoes = {
                "1": self.cadastrar_aluno,
                "2": self.cadastrar_disciplina,
                "3": self.registrar_notas,
                "4": self.registrar_frequencia,
                "5": self.gerar_boletim,
                "6": self.listar_alunos,
                "7": self.consultar_status,
                "8": self.remover_disciplina,
                "9": self.remover_aluno,
                "0": self.sair,
            }

            # acoes.get(opcao) tenta buscar a função correspondente à chave no dicionário.
            # Se a opção não existir, retorna None.
            acao = acoes.get(opcao)
            if acao:
                # Executa a função correspondente
                acao()
            else:
                print("\n  ❌ Opção inválida. Tente novamente.")

    # ── 1. Cadastrar Aluno ───────────────────────────────────────────

    def cadastrar_aluno(self) -> None:
        """Cadastra um novo aluno no sistema e salva na persistência JSON."""
        print("\n  ─── Cadastro de Aluno ───")

        # Lê a matrícula como string tratada
        matricula = self.validadores.ler_string("  Matrícula: ")
        
        # Valida se a matrícula é composta apenas de letras e números (isalnum)
        if not self.validadores.validar_matricula(matricula):
            print("  ❌ Matrícula inválida. Use apenas letras e números.")
            return

        # Verifica se já existe um aluno na lista com a mesma matrícula cadastrada
        if self.persistencia.buscar_aluno(self.alunos, matricula):
            print(f"  ❌ Já existe um aluno com a matrícula '{matricula}'.")
            return

        # Lê o nome do aluno, exigindo um comprimento mínimo de 2 caracteres
        nome = self.validadores.ler_string("  Nome completo: ", minimo=2)
        if not self.validadores.validar_nome(nome):
            print("  ❌ Nome inválido. Deve ter pelo menos 2 caracteres.")
            return

        # Cria uma nova instância de Aluno e adiciona na lista 'self.alunos'
        aluno = Aluno(matricula=matricula, nome=nome)
        self.alunos.append(aluno)
        
        # Salva o estado atualizado no arquivo JSON
        self.persistencia.salvar(self.alunos)

        print(f"\n  ✅ Aluno '{nome}' (matrícula: {matricula}) cadastrado com sucesso!")

    # ── 2. Cadastrar Disciplina ──────────────────────────────────────

    def cadastrar_disciplina(self) -> None:
        """Cadastra uma disciplina vinculada a um aluno específico."""
        print("\n  ─── Cadastro de Disciplina ───")

        # Método auxiliar para escolher um aluno. Se retornar None, interrompe a operação.
        aluno = self._selecionar_aluno()
        if aluno is None:
            return

        # Pede o nome da matéria/disciplina
        nome_disciplina = self.validadores.ler_string("  Nome da disciplina: ", minimo=2)

        try:
            # Cria a instância da Disciplina
            disciplina = Disciplina(nome=nome_disciplina)
            
            # Adiciona a disciplina à lista de disciplinas do aluno.
            # O método 'adicionar_disciplina' valida se o aluno já cursa a matéria e
            # pode lançar um ValueError se já estiver cadastrado.
            aluno.adicionar_disciplina(disciplina)
            
            # Salva o arquivo JSON atualizado
            self.persistencia.salvar(self.alunos)
            print(
                f"\n  ✅ Disciplina '{nome_disciplina}' adicionada para "
                f"'{aluno.nome}'!"
            )
        except ValueError as e:
            # Captura o erro disparado pela classe Aluno caso a disciplina seja duplicada
            print(f"\n  ❌ {e}")

    # ── 3. Registrar Notas ───────────────────────────────────────────

    def registrar_notas(self) -> None:
        """Registra as 3 notas de uma disciplina para o aluno selecionado."""
        print("\n  ─── Registro de Notas ───")

        # Seleciona o aluno
        aluno = self._selecionar_aluno()
        if aluno is None:
            return

        # Seleciona a disciplina pertencente a este aluno
        disciplina = self._selecionar_disciplina(aluno)
        if disciplina is None:
            return

        # Se já existem 3 notas cadastradas, pergunta se deseja sobrescrevê-las
        if disciplina.notas_completas:
            resposta = input(
                "  ⚠️  Notas já registradas. Deseja substituir? (s/n): "
            ).strip().lower()
            if resposta != "s":
                print("  Operação cancelada.")
                return
            # Limpa as notas anteriores para receber as novas
            disciplina.notas.clear()

        print(f"\n  Registrando notas para '{disciplina.nome}':")
        print("  (Notas devem estar entre 0.0 e 10.0)\n")

        # Loop para ler exatamente as 3 notas requeridas
        for i in range(3):
            # 'ler_float' garante que a entrada do terminal será um número decimal válido entre 0.0 e 10.0
            nota = self.validadores.ler_float(
                f"  Nota {i + 1} (N{i + 1}): ", minimo=0.0, maximo=10.0
            )
            disciplina.notas.append(nota)

        # Salva o estado atualizado no arquivo JSON
        self.persistencia.salvar(self.alunos)
        
        # Calcula a média aritmética e imprime
        media = Calculadora.calcular_media(disciplina.notas)
        print(f"\n  ✅ Notas registradas! Média: {media:.2f}")

    # ── 4. Registrar Frequência ──────────────────────────────────────

    def registrar_frequencia(self) -> None:
        """Registra a frequência (aulas ministradas e presenças) em uma disciplina de um aluno."""
        print("\n  ─── Registro de Frequência ───")

        # Seleciona o aluno e a matéria
        aluno = self._selecionar_aluno()
        if aluno is None:
            return

        disciplina = self._selecionar_disciplina(aluno)
        if disciplina is None:
            return

        # Lê os dados do console, garantindo valores inteiros válidos
        total_aulas = self.validadores.ler_int(
            "  Total de aulas ministradas: ", minimo=1, maximo=999
        )
        # O número de aulas assistidas não pode ultrapassar o total de aulas ministradas
        aulas_assistidas = self.validadores.ler_int(
            "  Aulas assistidas pelo aluno: ", minimo=0, maximo=total_aulas
        )

        # Atualiza o objeto da disciplina com as informações de frequência
        disciplina.aulas_total = total_aulas
        disciplina.aulas_assistidas = aulas_assistidas
        
        # Grava as alterações no banco de dados JSON
        self.persistencia.salvar(self.alunos)

        # Calcula a frequência percentual e valida se atende ao limite mínimo de 75%
        frequencia = Calculadora.calcular_frequencia(aulas_assistidas, total_aulas)
        status_freq = "✅ Dentro do mínimo" if frequencia >= 75.0 else "❌ Abaixo do mínimo (75%)"
        print(f"\n  ✅ Frequência registrada: {frequencia:.1f}% — {status_freq}")

    # ── 5. Gerar Boletim ─────────────────────────────────────────────

    def gerar_boletim(self) -> None:
        """Gera e exibe o boletim completo do aluno selecionado."""
        print("\n  ─── Boletim Final ───")

        aluno = self._selecionar_aluno()
        if aluno is None:
            return

        # Verifica se o aluno possui alguma disciplina cadastrada
        if not aluno.disciplinas:
            print("  ⚠️  Este aluno não possui disciplinas cadastradas.")
            return

        # Delega ao serviço 'GeradorBoletim' a construção textual da tabela em ASCII
        boletim = GeradorBoletim.gerar(aluno)
        print()
        print(boletim)

    # ── 6. Listar Alunos ─────────────────────────────────────────────

    def listar_alunos(self) -> None:
        """Lista todos os alunos cadastrados em formato de lista simples."""
        print("\n  ─── Alunos Cadastrados ───")

        if not self.alunos:
            print("  ⚠️  Nenhum aluno cadastrado.")
            return

        # Mostra o total de registros na lista
        print(f"\n  Total: {len(self.alunos)} aluno(s)\n")
        for aluno in self.alunos:
            # Imprime a representação do objeto Aluno definida em seu método __str__
            print(f"    {aluno}")

    # ── 7. Consultar Status ──────────────────────────────────────────

    def consultar_status(self) -> None:
        """Consulta o status final de aprovação em uma disciplina selecionada."""
        print("\n  ─── Consulta de Status ───")

        aluno = self._selecionar_aluno()
        if aluno is None:
            return

        disciplina = self._selecionar_disciplina(aluno)
        if disciplina is None:
            return

        # Determina o status com base na média e frequência cadastrada
        status = Calculadora.determinar_status(disciplina)

        # Formatação visual com caixas de texto no console usando especificadores de largura (ex: :<33)
        # :<33 significa alinhar o texto à esquerda preenchendo com espaços até somar 33 caracteres
        # :.2f indica número real/float com duas casas decimais
        # :.1f indica número real/float com uma casa decimal
        print(f"\n  ┌─────────────────────────────────────────┐")
        print(f"  │ Aluno: {aluno.nome:<33}│")
        print(f"  │ Disciplina: {disciplina.nome:<28}│")
        print(f"  │                                         │")

        if disciplina.media is not None:
            print(f"  │ Média: {disciplina.media:<33.2f}│")
        else:
            print(f"  │ Média: {'N/A':<33}│")

        if disciplina.frequencia is not None:
            print(f"  │ Frequência: {disciplina.frequencia:<28.1f}│")
        else:
            print(f"  │ Frequência: {'N/A':<28}│")

        print(f"  │                                         │")
        print(f"  │ Status: {status:<32}│")
        print(f"  └─────────────────────────────────────────┘")

    # ── 8. Remover Disciplina ────────────────────────────────────────

    def remover_disciplina(self) -> None:
        """Remove uma disciplina da grade curricular do aluno selecionado."""
        print("\n  ─── Remover Disciplina ───")

        aluno = self._selecionar_aluno()
        if aluno is None:
            return

        disciplina = self._selecionar_disciplina(aluno)
        if disciplina is None:
            return

        # Solicita confirmação explícita antes de deletar
        resposta = input(
            f"  ⚠️  Tem certeza que deseja remover '{disciplina.nome}' "
            f"de '{aluno.nome}'? (s/n): "
        ).strip().lower()

        if resposta != "s":
            print("  Operação cancelada.")
            return

        # Remove o objeto disciplina da lista do aluno e persiste a alteração
        aluno.disciplinas.remove(disciplina)
        self.persistencia.salvar(self.alunos)
        print(
            f"\n  ✅ Disciplina '{disciplina.nome}' removida de "
            f"'{aluno.nome}' com sucesso!"
        )

    # ── 9. Remover Aluno ─────────────────────────────────────────────

    def remover_aluno(self) -> None:
        """Exclui completamente o cadastro de um aluno do sistema."""
        print("\n  ─── Remover Aluno ───")

        aluno = self._selecionar_aluno()
        if aluno is None:
            return

        # Exibe um resumo das dependências cadastradas do aluno antes de remover
        qtd_disc = len(aluno.disciplinas)
        print(f"\n  Aluno: {aluno.nome}")
        print(f"  Matrícula: {aluno.matricula}")
        print(f"  Disciplinas cadastradas: {qtd_disc}")

        resposta = input(
            f"\n  ⚠️  Tem certeza que deseja remover este aluno "
            f"e TODOS os seus dados? (s/n): "
        ).strip().lower()

        if resposta != "s":
            print("  Operação cancelada.")
            return

        # Remove da lista em memória e grava no arquivo JSON
        self.alunos.remove(aluno)
        self.persistencia.salvar(self.alunos)
        print(
            f"\n  ✅ Aluno '{aluno.nome}' (matrícula: {aluno.matricula}) "
            f"removido com sucesso!"
        )

    # ── 0. Sair ──────────────────────────────────────────────────────

    def sair(self) -> None:
        """Salva todas as alterações pendentes em disco e finaliza o interpretador."""
        self.persistencia.salvar(self.alunos)
        print("\n  💾 Dados salvos com sucesso!")
        print("  👋 Até logo! Obrigado por usar o EduGrade.\n")
        
        # Finaliza o processo Python com código 0 (sucesso)
        sys.exit(0)

    # ── Métodos Auxiliares (Privados) ─────────────────────────────────

    def _selecionar_aluno(self) -> Aluno | None:
        """Pede a matrícula no terminal e retorna a instância de Aluno.

        Returns:
            O objeto Aluno encontrado ou None se não for localizado.
        """
        if not self.alunos:
            print("  ⚠️  Nenhum aluno cadastrado. Cadastre um aluno primeiro.")
            return None

        matricula = input("  Matrícula do aluno: ").strip()
        aluno = self.persistencia.buscar_aluno(self.alunos, matricula)

        if aluno is None:
            print(f"  ❌ Aluno com matrícula '{matricula}' não encontrado.")
            return None

        print(f"  → Aluno selecionado: {aluno.nome}")
        return aluno

    def _selecionar_disciplina(self, aluno: Aluno) -> Disciplina | None:
        """Lista as disciplinas do aluno e solicita a seleção de uma delas.

        Args:
            aluno: O objeto Aluno selecionado.

        Returns:
            O objeto Disciplina encontrado ou None.
        """
        if not aluno.disciplinas:
            print(
                f"  ⚠️  '{aluno.nome}' não possui disciplinas cadastradas."
            )
            return None

        # Exibe as disciplinas cadastradas para o aluno com índice
        print("\n  Disciplinas disponíveis:")
        # 'enumerate(..., 1)' retorna o elemento e o índice começando em 1
        for i, disc in enumerate(aluno.disciplinas, 1):
            print(f"    {i}. {disc.nome}")

        nome_disciplina = input("\n  Nome da disciplina: ").strip()
        disciplina = aluno.buscar_disciplina(nome_disciplina)

        if disciplina is None:
            print(f"  ❌ Disciplina '{nome_disciplina}' não encontrada.")
            return None

        return disciplina


# ── Ponto de Entrada do Script ────────────────────────────────────────

# Esta validação garante que o código abaixo só seja executado se o arquivo for rodado
# diretamente pelo terminal (ex: python antiGTest.py). Se ele for importado como módulo
# por outro arquivo, o bloco não executa automaticamente.
if __name__ == "__main__":
    try:
        # Cria a instância principal do sistema e inicia a execução
        app = EduGrade()
        app.executar()
    except KeyboardInterrupt:
        # Captura o sinal de interrupção do teclado (Ctrl+C no console)
        # Evita a exibição do rastreamento de pilha (Traceback) do Python
        print("\n\n  👋 Programa encerrado pelo usuário.")
        sys.exit(0)
