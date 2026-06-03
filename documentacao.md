# Projeto EduGrade — Sistema de Gerenciamento Escolar

> Documentação de Requisitos e Arquitetura do Projeto
> Data de Criação: 2026-05-29
> Autores: Kauan Andrade, Luis Otavio
> Versão: 2.4

---

## 1. Visão Geral do Projeto

O **EduGrade** é um sistema de gestão escolar desenvolvido em Python (CLI) que permite o cadastro de alunos e disciplinas, o lançamento de notas e frequências, e a geração de boletins detalhados com o status final de cada aluno por disciplina. O sistema é voltado para professores e coordenadores que precisam de uma ferramenta simples e rápida para acompanhar o desempenho acadêmico de suas turmas.

---

## 1.1 Briefing do Projeto

| Campo | Descrição |
|---|---|
| **Cliente (papel)** | Professor da disciplina / Coordenador pedagógico |
| **Problema** | Gestão manual de notas e frequências é propensa a erros e dificulta a visualização rápida do status dos alunos. |
| **Solução Proposta** | Sistema CLI que centraliza cadastros, cálculos de média e frequência, e emissão de boletins automatizados. |
| **Escopo (IN)** | Cadastro de alunos, lançamento de notas (N1/N2/N3), controle de frequência, cálculo de média, boletim individual e por turma. |
| **Escopo (OUT)** | Comunicação com pais, sistema web, autenticação multi-usuário, histórico por ano letivo. |
| **Tecnologia** | Python 3 (CLI), estruturas de dicionários e listas, persistência em arquivo JSON. |

---

## 2. Regras de Negócio (RN)

### RN-01 — Cálculo de Média

- Cada disciplina possui 3 notas: N1, N2 e N3.
- Nota não lançada é tratada como 0.0.
- Fórmula: `Média = (N1 + N2 + N3) / 3`
- Cada nota deve estar no intervalo **[0.0, 10.0]**. Valores fora deste intervalo são rejeitados.

### RN-02 — Lógica de Aprovação / Recuperação / Reprovação por Nota

| Condição de Média | Status Final |
|---|---|
| Média >= 7.0 | ✅ Aprovado |
| 5.0 <= Média < 7.0 | ⚠️ Recuperação |
| Média < 5.0 | ❌ Reprovado por Nota |

### RN-03 — Frequência Mínima Obrigatória

- O aluno deve ter no mínimo **75%** de presença em cada disciplina.
- Fórmula: `Frequência (%) = (Aulas Assistidas / Total de Aulas) × 100`
- Se frequência < 75%, o status final é **Reprovado por Falta**, independentemente da média.
- A verificação de frequência tem **prioridade** sobre o cálculo de média.

---

## 3. Histórias de Usuário (User Stories)

> Formato: *"Como [Ator], eu quero [Funcionalidade] para [Valor de Negócio]."*

---

### US-01 — Cadastrar Aluno

**História:** Como professor, eu quero cadastrar um novo aluno informando nome, matrícula e turma, para que ele possa ter suas notas e frequência registradas no sistema.

**Critérios de Aceite:**

- **CA-01:** Dado que o professor informa nome, matrícula e turma válidos, quando confirmar o cadastro, então o aluno deve aparecer na listagem da turma.
- **CA-02:** Dado que a matrícula já existe, quando tentar cadastrar novamente, então o sistema deve exibir `"Matrícula já cadastrada"` e não duplicar o registro.

---

### US-02 — Lançar Notas

**História:** Como professor, eu quero lançar as três notas (N1, N2, N3) de um aluno em uma disciplina, para que o sistema calcule automaticamente a média e o status.

**Critérios de Aceite:**

- **CA-01:** Dado que o professor informa três notas entre 0.0 e 10.0, quando confirmar, então o sistema deve calcular e exibir a média e o status (Aprovado / Recuperação / Reprovado).
- **CA-02:** Dado que uma nota informada está fora do intervalo [0.0, 10.0], então o sistema deve rejeitar a entrada com mensagem de erro clara.
- **CA-03:** Dado que o professor não informar uma das notas, então o sistema deve considerar o valor 0.0 para aquela nota no cálculo.

---

### US-03 — Registrar Frequência

**História:** Como professor, eu quero registrar o número de aulas assistidas e o total de aulas de um aluno em uma disciplina, para que o sistema calcule a frequência e valide o critério de presença.

**Critérios de Aceite:**

- **CA-01:** Dado que o aluno tem frequência >= 75%, então o status de frequência é "Regular" e a média é considerada para aprovação.
- **CA-02:** Dado que o aluno tem frequência < 75%, então o status final deve ser "Reprovado por Falta", mesmo que a média seja >= 7.0.
- **CA-03:** Dado que o número de aulas assistidas é maior que o total de aulas, então o sistema deve rejeitar a entrada como inválida.

---

### US-04 — Consultar Boletim Individual

**História:** Como coordenador, eu quero consultar o boletim completo de um aluno informando sua matrícula, para visualizar suas notas, média, frequência e status em todas as disciplinas.

**Critérios de Aceite:**

- **CA-01:** Dado que a matrícula existe, quando o boletim for solicitado, então o sistema exibe nome, turma, e para cada disciplina: N1, N2, N3, média, frequência e status final.
- **CA-02:** Dado que a matrícula não existe, então o sistema deve exibir `"Aluno não encontrado"`.

---

### US-05 — Listar Alunos por Turma

**História:** Como professor, eu quero listar todos os alunos de uma turma específica, para ter uma visão geral da turma com nome e matrícula.

**Critérios de Aceite:**

- **CA-01:** Dado que a turma possui alunos cadastrados, então o sistema exibe a lista com nome e matrícula de cada aluno, ordenada alfabeticamente.
- **CA-02:** Dado que a turma não possui nenhum aluno, então o sistema exibe `"Nenhum aluno cadastrado nesta turma"`.

---

## 4. Requisitos Funcionais (RF)

| ID | Nome | Descrição |
|---|---|---|
| RF-001 | Cadastro de Aluno | O sistema deve permitir o cadastro de um novo aluno com nome completo, matrícula e turma. |
| RF-002 | Validação de Matrícula Única | O sistema deve garantir que não existam dois alunos com a mesma matrícula. |
| RF-003 | Consulta por Matrícula | O sistema deve permitir buscar dados de um aluno informando sua matrícula. |
| RF-004 | Listagem por Turma | O sistema deve listar todos os alunos de uma turma com nome e matrícula. |
| RF-005 | Atualização de Dados | O sistema deve permitir alterar o nome do aluno ou transferi-lo de turma. |
| RF-006 | Lançamento de Notas | O sistema deve permitir registrar N1, N2 e N3 de um aluno por disciplina, calculando a média automaticamente. |
| RF-007 | Validação de Notas | O sistema deve rejeitar notas fora do intervalo [0.0, 10.0] com mensagem de erro. |
| RF-008 | Registro de Frequência | O sistema deve registrar aulas assistidas e total de aulas, calculando o percentual de frequência. |
| RF-009 | Cálculo de Status Final | O sistema deve determinar o status do aluno (Aprovado / Recuperação / Reprovado por Nota / Reprovado por Falta) aplicando as RNs na ordem correta. |
| RF-010 | Emissão de Boletim | O sistema deve gerar o boletim individual do aluno com todas as disciplinas, notas, médias, frequências e status. |

---

## 5. Requisitos Não Funcionais (RNF)

| ID | Descrição |
|---|---|
| RNF-01 | O sistema deve rodar via terminal (CLI), sem necessidade de interface gráfica. |
| RNF-02 | Entradas inválidas (letras onde se espera número, valores fora do intervalo) devem ser rejeitadas com mensagem clara ao usuário. |
| RNF-03 | O código deve ser modular, com funções separadas por responsabilidade (ex: função de cálculo de média separada da função de exibição de boletim). |
| RNF-04 | Os dados devem ser persistidos em arquivo JSON para que não sejam perdidos ao fechar o programa. |
| RNF-05 | O sistema não deve travar em nenhuma situação de entrada inválida — nenhum erro não tratado deve ser exibido ao usuário final. |

---

## 6. Protótipo de Fluxo CLI

### 6.1 Menu Principal

```
================================
     BEM-VINDO AO EDUGRADE
================================
[1] Gerenciar Alunos
[2] Lançar Notas e Frequência
[3] Consultar Boletim
[4] Listar Turma
[0] Sair
Escolha uma opção: _
```

### 6.2 Fluxo: Cadastrar Aluno

```
--- CADASTRO DE ALUNO ---
Nome completo: João Silva
Número de matrícula: 2024001
Turma: 3A
> Aluno cadastrado com sucesso!
```

Erro esperado (matrícula duplicada):
```
> ERRO: Matrícula 2024001 já está cadastrada.
```

### 6.3 Fluxo: Lançamento de Notas

```
--- LANÇAMENTO DE NOTAS ---
Matrícula do aluno: 2024001
Disciplina: Matemática
Nota N1 (0 a 10): 7.5
Nota N2 (0 a 10): 6.0
Nota N3 (0 a 10): 8.0
Aulas assistidas: 32
Total de aulas: 40
--------------------------
Média calculada : 7.17
Frequência      : 80.0%
Status          : APROVADO
--------------------------
```

Erro esperado (nota inválida):
```
> ERRO: Nota inválida. Informe um valor entre 0.0 e 10.0.
```

### 6.4 Fluxo: Boletim Individual

```
--- BOLETIM DO ALUNO ---
Matrícula : 2024001
Nome      : João Silva  |  Turma: 3A
================================================
Disciplina    N1   N2   N3   Média  Freq.  Status
Matemática   7.5  6.0  8.0   7.17  80.0%  APROVADO
Português    5.0  4.5  6.0   5.17  70.0%  REP. FALTA
História     4.0  3.5  4.5   4.00  90.0%  REP. NOTA
================================================
```

---

## 7. Backlog e Kanban

> Quadro Kanban: **Backlog | To Do | Doing | Done**

| ID | Tarefa / História | Sprint | Responsável | Prioridade |
|---|---|---|---|---|
| T-01 | Estrutura do projeto e menu principal | Sprint 1 | Kauan | Alta |
| T-02 | Função de cadastro de aluno + validação de matrícula | Sprint 2 | Luis | Alta |
| T-03 | Função de listagem e consulta por matrícula | Sprint 2 | Luis | Alta |
| T-04 | Função de lançamento de notas com validação | Sprint 2 | Kauan | Alta |
| T-05 | Função de cálculo de média e status por nota | Sprint 2 | Kauan | Alta |
| T-06 | Função de registro e cálculo de frequência | Sprint 2 | Luis | Alta |
| T-07 | Lógica de status final (frequência tem prioridade) | Sprint 3 | Kauan | Alta |
| T-08 | Geração de boletim individual formatado | Sprint 3 | Luis | Alta |
| T-09 | Persistência de dados em arquivo JSON | Sprint 3 | Kauan | Média |
| T-10 | Tratamento global de erros de entrada (try/except) | Sprint 4 | Luis | Média |
| T-11 | Função de atualização de dados do aluno | Sprint 4 | Ambos | Baixa |

---

## 8. Review & Retrospectiva

### 8.1 O que funcionou bem?

- **Arquitetura Modular:** A separação em camadas (`models`, `services`, `utils`) facilitou o desenvolvimento independente e a organização de código limpo.
- **Validação Robusta:** O módulo `validadores` impediu travamentos e entradas inválidas, garantindo a estabilidade exigida no requisito RNF-05.
- **Persistência Simples:** A persistência usando JSON puro em `dados/alunos.json` resolveu o problema sem necessidade de bancos de dados complexos.

### 8.2 O que foi mais difícil?

- **Prioridade de Regras de Negócio:** A aplicação correta da regra RN-03 (onde a frequência menor que 75% reprova o aluno diretamente, independentemente da nota) exigiu atenção especial na ordem de precedência da `Calculadora`.
- **Formatação Visual:** O alinhamento dinâmico e formatação da tabela ASCII do boletim no terminal com base no tamanho das strings de nomes e disciplinas.

### 8.3 O que fariam diferente?

- **Testes Automatizados:** Implementar testes de unidade (com `pytest` ou `unittest`) para garantir que as regras de média e aprovação funcionem sem regressões.
- **Interface Gráfica (GUI):** Oferecer uma alternativa de interface visual mais rica ou web para o usuário, no lugar da CLI pura.

### 8.4 Lições Aprendidas

- A separação de responsabilidades (por exemplo, desacoplar cálculo de média em um serviço `Calculadora` isolado dos modelos) simplifica as alterações futuras e protege o domínio do projeto.

---

## 9. Estrutura do Projeto

O sistema está organizado de acordo com a seguinte árvore de diretórios:

```text
ProjetoFinal_LER/
│
├── main.py                  # Ponto de entrada principal do programa (Entrypoint CLI)
├── antiGTest.py             # Arquivo com a classe principal do sistema (EduGrade)
├── documentacao.md          # Este arquivo de documentação de requisitos e especificações
├── requirements.txt         # Arquivo contendo dependências do Python (caso aplicável)
│
├── dados/
│   └── alunos.json          # Arquivo gerado para salvar o banco de dados dos alunos cadastrados
│
├── models/
│   ├── __init__.py
│   ├── aluno.py             # Modelo de dados da classe Aluno (com métodos to_dict e from_dict)
│   └── disciplina.py        # Modelo de dados da classe Disciplina (notas, presença, propriedades)
│
├── services/
│   ├── __init__.py
│   ├── boletim.py           # Serviço de geração e renderização do Boletim em tabela ASCII
│   ├── calculadora.py       # Centraliza as regras de negócio de aprovação por nota/frequência
│   └── persistencia.py      # Serviço de salvamento e carregamento de JSON em arquivos locais
│
└── utils/
    ├── __init__.py
    └── validadores.py       # Funções utilitárias de leitura com validação de tipos de dados
```

---

## 10. Manual de Execução

### Pré-requisitos
*   Python 3.10 ou superior instalado na máquina.

### Como Executar
1. Abra o terminal (PowerShell, Command Prompt ou Terminal do Linux/macOS) na pasta raiz do projeto:
   ```
   Entre na pasta do projeto 
   Ex: C:\Users\1devsesi46a\Documents\Workspace\ProjetoFinal_LER
   ```
2. Execute o programa principal:
   ```bash
   python main.py
   ```
3. Utilize os números do teclado de **0** a **9** para interagir com o menu do console. Todos os dados digitados serão gravados automaticamente em `dados/alunos.json` ao sair.

---

## Histórico de Versões

| Versão | Data | Autores | Alterações |
|---|---|---|---|
| 1.0 | 2026-05-29 | Kauan, Luis | Versão inicial com RN, RF e RNF. |
| 1.1 | 2026-06-03 | Kauan, Luis | Adição de User Stories, critérios de aceite, RFs completos, protótipo CLI e backlog. |
| 1.2 | 2026-06-03 | Kauan, Luis | Projeto finalizado e pronto para uso, porém pendente de testes formais de homologação. |
| 2.0 | 2026-06-03 | Kauan, Luis | Inicio do projeto e criação de bibliotecas locais com o uso do Antigravity. |
| 2.1 | 2026-06-03 | Kauan, Luis | Bibliotecas prontas e inicio do projeto principal. |
| 2.2 | 2026-06-03 | Kauan, Luis | Projeto finalizado e pronto para uso, porém pendente de testes de usuario. |
| 2.3 | 2026-06-03 | Antigravity, Kauan, Luis | Preenchimento de Review e Retrospectiva, documentação da estrutura física de diretórios e inclusão do manual de execução. |
| 2.4 | 2026-06-03 | Antigravity, Kauan, Luis | Criação do arquivo principal simplificado main.py (entrypoint) e atualização da documentação. |