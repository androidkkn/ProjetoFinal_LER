# 🏃 Sprint Backlog — EduGrade

**Produto:** EduGrade — Sistema de Gestão de Notas Escolares  
**Equipe:** Kauan Andrade, Luis Otavio  
**Duração de cada Sprint:** 2 semanas  
**Última atualização:** 12/06/2026  
**Versão do Produto:** 2.5  

---

## Definição de Pronto (Definition of Done — DoD)

Para que uma tarefa seja considerada **Concluída**, ela deve atender a todos os critérios abaixo:

- [x] Código implementado sem erros de sintaxe
- [x] Validações de entrada implementadas (notas 0–10, frequência, matrícula alfanumérica)
- [x] Dados persistidos corretamente no `dados/alunos.json`
- [x] Testado manualmente com cenários positivos e negativos
- [x] Código documentado com docstrings e comentários em português
- [x] Estrutura modular respeitada (`models/`, `services/`, `utils/`)

---

## Sprint 1 — Estrutura e Cadastro Base

**Período:** 15/05/2026 a 28/05/2026  
**Objetivo:** Montar a arquitetura do projeto, criar modelos de dados e implementar cadastro de alunos com persistência.  
**Status:** ✅ Concluída  
**Pontos planejados:** 18 | **Pontos entregues:** 18  

| ID     | Tarefa / User Story                          | Responsável | Pontos | Status        |
|--------|----------------------------------------------|-------------|--------|---------------|
| T-01   | Criar estrutura de pastas (`models/`, `services/`, `utils/`, `dados/`) | Kauan | 1 | ✅ Concluído |
| T-02   | Implementar modelo `Disciplina` (`dataclass`, propriedades `media`, `frequencia`, `notas_completas`, serialização) | Kauan | 3 | ✅ Concluído |
| T-03   | Implementar modelo `Aluno` (`dataclass`, `adicionar_disciplina`, `buscar_disciplina`, serialização) | Kauan | 3 | ✅ Concluído |
| T-04   | Implementar `Persistencia` (salvar/carregar JSON, `buscar_aluno`, tratamento de erros) | Kauan | 3 | ✅ Concluído |
| T-05   | Implementar `Validadores` (`validar_nota`, `validar_frequencia`, `validar_matricula`, `validar_nome`, `ler_float`, `ler_int`, `ler_string`) | Kauan | 3 | ✅ Concluído |
| T-06   | Criar menu principal interativo com padrão Dispatcher em `ProjetoFinal.py` | Kauan | 2 | ✅ Concluído |
| US-01  | Cadastrar aluno (nome + matrícula)           | Luis        | 3      | ✅ Concluído  |

### Entregáveis da Sprint 1

| Arquivo Criado/Modificado                  | Descrição                                       |
|--------------------------------------------|-------------------------------------------------|
| `models/__init__.py`                       | Exports de `Aluno` e `Disciplina`               |
| `models/disciplina.py`                     | Dataclass com propriedades calculadas (85 linhas)|
| `models/aluno.py`                          | Dataclass com gerenciamento de disciplinas (84 linhas) |
| `services/__init__.py`                     | Exports de `Calculadora`, `GeradorBoletim`, `Persistencia` |
| `services/persistencia.py`                 | CRUD JSON com tratamento de erros (83 linhas)   |
| `utils/__init__.py`                        | Export de `Validadores`                         |
| `utils/validadores.py`                     | 6 métodos de validação de entrada (121 linhas)  |
| `ProjetoFinal.py` (parcial)               | Menu CLI com opção 1 funcional                  |

### Retrospectiva — Sprint 1

| 😊 O que foi bem                                | 😐 O que pode melhorar                   |
|--------------------------------------------------|------------------------------------------|
| Arquitetura modular definida desde o início       | Faltou criar testes automatizados        |
| Serialização JSON `to_dict`/`from_dict` funcional | Documentação ainda não existia           |
| Validadores robustos com loops de re-entrada      | `requirements.txt` ainda vazio           |

---

## Sprint 2 — Notas, Frequência e Regras de Negócio

**Período:** 29/05/2026 a 11/06/2026  
**Objetivo:** Implementar o registro de notas e frequência, criar a `Calculadora` com todas as regras de negócio (RN-01 a RN-03), e gerar o boletim formatado.  
**Status:** ✅ Concluída  
**Pontos planejados:** 30 | **Pontos entregues:** 30  

| ID     | Tarefa / User Story                                                     | Responsável | Pontos | Status        |
|--------|-------------------------------------------------------------------------|-------------|--------|---------------|
| US-02  | Validar matrícula única no cadastro                                     | Luis        | 2      | ✅ Concluído  |
| US-07  | Cadastrar disciplinas para um aluno                                     | Kauan       | 3      | ✅ Concluído  |
| US-08  | Impedir disciplinas duplicadas (comparação case-insensitive)            | Kauan       | 2      | ✅ Concluído  |
| US-12  | Registrar 3 notas (N1, N2, N3) por disciplina                          | Kauan       | 5      | ✅ Concluído  |
| US-13  | Validar notas entre 0.0 e 10.0                                         | Kauan       | 2      | ✅ Concluído  |
| US-14  | Permitir substituição de notas já registradas                           | Kauan       | 3      | ✅ Concluído  |
| US-17  | Registrar frequência (aulas assistidas / total)                         | Luis        | 3      | ✅ Concluído  |
| US-18  | Validar aulas assistidas ≤ total de aulas                              | Luis        | 2      | ✅ Concluído  |
| T-07   | Implementar `Calculadora` (`calcular_media`, `calcular_frequencia`, `determinar_status`) e constantes `Status` | Kauan | 5 | ✅ Concluído |
| T-08   | Implementar `GeradorBoletim` (tabela ASCII, legenda, resumo)           | Kauan        | 5      | ✅ Concluído  |

### Entregáveis da Sprint 2

| Arquivo Criado/Modificado                  | Descrição                                       |
|--------------------------------------------|-------------------------------------------------|
| `services/calculadora.py`                  | `Calculadora` + `Status` — 105 linhas com 3 métodos e 5 constantes de status |
| `services/boletim.py`                      | `GeradorBoletim` — 163 linhas, tabela formatada com box-drawing, legenda e resumo |
| `ProjetoFinal.py` (expandido)              | Opções 2–7 implementadas: cadastro disciplina, registrar notas, frequência, boletim, listar alunos, consultar status |

### Regras de Negócio Implementadas

| Regra  | Implementação em `calculadora.py`                               | Validação                         |
|--------|------------------------------------------------------------------|-----------------------------------|
| RN-01  | `calcular_media()`: `sum(notas) / len(notas)`                   | Rejeita lista vazia com ValueError |
| RN-02  | `determinar_status()`: Média ≥ 7.0 → APROVADO, ≥ 5.0 → RECUPERAÇÃO, < 5.0 → REPROVADO DIRETO | 3 faixas com constantes `MEDIA_APROVACAO` e `MEDIA_RECUPERACAO` |
| RN-03  | `determinar_status()`: Frequência < 75% verificada **antes** da média → REPROVADO POR FALTA | Constante `FREQUENCIA_MINIMA = 75.0` |

### Retrospectiva — Sprint 2

| 😊 O que foi bem                                     | 😐 O que pode melhorar                         |
|-------------------------------------------------------|-------------------------------------------------|
| Todas as 3 regras de negócio implementadas corretamente | Boletim com problemas de encoding UTF-8 no Windows (cp1252) |
| Boletim formatado com legenda e resumo estatístico     | Código de `ProjetoFinal.py` ficou extenso (350+ linhas) |
| Frequência verificada antes da média (RN-03 respeitada) | Faltam testes unitários automatizados           |
| Feedback visual imediato ao registrar notas e frequência | Não há opção de desfazer ações                 |

---

## Sprint 3 — Remoções, Documentação e Entrypoint

**Período:** 29/05/2026 a 12/06/2026  
**Objetivo:** Adicionar opções de remoção (disciplina e aluno), criar documentação completa e simplificar o ponto de entrada.  
**Status:** ✅ Concluída  
**Pontos planejados:** 22 | **Pontos entregues:** 22  

| ID     | Tarefa / User Story                                                     | Responsável | Pontos | Status        |
|--------|-------------------------------------------------------------------------|-------------|--------|---------------|
| US-03  | Listar todos os alunos cadastrados                                      | Kauan       | 2      | ✅ Concluído  |
| US-04  | Remover aluno por matrícula (com confirmação e resumo)                  | Kauan       | 3      | ✅ Concluído  |
| US-09  | Remover disciplina de um aluno (com confirmação)                        | Kauan       | 3      | ✅ Concluído  |
| US-10  | Visualizar disciplinas disponíveis ao selecionar aluno                  | Kauan       | 2      | ✅ Concluído  |
| US-15  | Exibir média imediatamente após registro de notas                       | Kauan       | 1      | ✅ Concluído  |
| US-19  | Alerta visual se frequência abaixo de 75%                               | Luis        | 1      | ✅ Concluído  |
| US-26  | Consultar status detalhado por disciplina (caixa formatada)             | Luis        | 2      | ✅ Concluído  |
| US-27  | Garantir prioridade da frequência sobre a média                         | Kauan       | 2      | ✅ Concluído  |
| US-39  | Criar protótipo simplificado (`prototip.py`)                            | Kauan       | 1      | ✅ Concluído  |
| US-40  | Documentar projeto completo no `README.md`                              | Ambos       | 2      | ✅ Concluído  |
| T-09   | Adicionar comentários explicativos em português em `ProjetoFinal.py`   | Kauan       | 2      | ✅ Concluído  |
| T-10   | Escrever `requirements.txt`                                             | Luis        | 1      | ✅ Concluído  |

### Entregáveis da Sprint 3

| Arquivo Criado/Modificado                  | Descrição                                       |
|--------------------------------------------|-------------------------------------------------|
| `ProjetoFinal.py` (final)                  | 479 linhas — opções 1 a 9 + sair, comentários detalhados em PT-BR |
| `prototip.py`                              | Protótipo em script único procedural, sem dependências externas |
| `README.md`                                | Documentação completa v2.4: briefing, RNs, user stories, RFs, RNFs, protótipo CLI, backlog, review, estrutura e manual |
| `requirements.txt`                         | Declaração de dependências (apenas stdlib)       |

### Retrospectiva — Sprint 3

| 😊 O que foi bem                                     | 😐 O que pode melhorar                         |
|-------------------------------------------------------|-------------------------------------------------|
| Funcionalidades de remoção com confirmação segura     | Faltam testes automatizados (pytest/unittest)   |
| README.md completo e profissional com versionamento    | Busca de aluno apenas por matrícula (não por nome) |
| Comentários em português facilitam leitura do código   | Não há funcionalidade de edição de dados         |
| Entrypoint limpo (`prototip.py`)                       | Exportação de boletim (PDF/CSV) não implementada |

---

## Sprint 4 — Melhorias e Expansões (Planejada)

**Período:** 13/06/2026 a 26/06/2026  
**Objetivo:** Implementar edição de dados, busca por nome, nota de recuperação e testes automatizados.  
**Status:** 📋 Planejada  
**Pontos planejados:** 22  

| ID     | Tarefa / User Story                                                     | Responsável | Pontos | Status        |
|--------|-------------------------------------------------------------------------|-------------|--------|---------------|
| US-05  | Editar nome de um aluno                                                 | Dev         | 2      | 📋 A Fazer    |
| US-06  | Buscar aluno pelo nome                                                  | Dev         | 3      | 📋 A Fazer    |
| US-11  | Editar nome de uma disciplina                                           | Dev         | 2      | 📋 A Fazer    |
| US-28  | Registrar nota de recuperação para alunos em recuperação                | Dev         | 5      | 📋 A Fazer    |
| US-41  | Implementar testes automatizados com pytest                             | Dev         | 5      | 📋 A Fazer    |
| US-43  | Relatório por turma                                                     | Dev         | 8      | 📋 A Fazer    |

### Tarefas Técnicas — Sprint 4

| ID      | Tarefa Técnica                                               | Pontos | Status        |
|---------|--------------------------------------------------------------|--------|---------------|
| TK-01   | Adicionar método `editar_nome()` em `Aluno`                  | 1      | 📋 A Fazer    |
| TK-02   | Adicionar método `buscar_por_nome()` em `Persistencia`       | 2      | 📋 A Fazer    |
| TK-03   | Adicionar lógica de nota de recuperação em `Calculadora`     | 3      | 📋 A Fazer    |
| TK-04   | Criar arquivo `tests/test_calculadora.py`                    | 3      | 📋 A Fazer    |
| TK-05   | Criar arquivo `tests/test_modelos.py`                        | 2      | 📋 A Fazer    |
| TK-06   | Implementar conceito de "Turma" nos modelos                  | 5      | 📋 A Fazer    |

---

## Sprint 5 — Exportação e Interface (Planejada)

**Período:** 27/06/2026 a 10/07/2026  
**Objetivo:** Implementar exportação de boletins e explorar interface gráfica.  
**Status:** 📋 Planejada  
**Pontos planejados:** 21  

| ID     | Tarefa / User Story                                                     | Responsável | Pontos | Status        |
|--------|-------------------------------------------------------------------------|-------------|--------|---------------|
| US-32  | Exportar boletim em PDF                                                 | Dev         | 8      | 📋 A Fazer    |
| US-33  | Exportar boletim em CSV                                                 | Dev         | 5      | 📋 A Fazer    |
| US-46  | Login com senha para proteger dados                                     | Dev         | 8      | 📋 A Fazer    |

### Tarefas Técnicas — Sprint 5

| ID      | Tarefa Técnica                                               | Pontos | Status        |
|---------|--------------------------------------------------------------|--------|---------------|
| TK-07   | Pesquisar biblioteca de PDF (fpdf2 ou reportlab)             | 1      | 📋 A Fazer    |
| TK-08   | Criar `services/exportador_csv.py`                           | 3      | 📋 A Fazer    |
| TK-09   | Criar `services/exportador_pdf.py`                           | 5      | 📋 A Fazer    |
| TK-10   | Implementar sistema de autenticação simples                  | 5      | 📋 A Fazer    |
| TK-11   | Atualizar `requirements.txt` com novas dependências          | 1      | 📋 A Fazer    |

---

## Burndown — Visão Geral

```
Pontos │
  30   │      ██
       │      ██
  25   │      ██
       │ ██   ██   ██
  20   │ ██   ██   ██          ▓▓
       │ ██   ██   ██          ▓▓          ▓▓
  15   │ ██   ██   ██          ▓▓          ▓▓
       │ ██   ██   ██          ▓▓          ▓▓
  10   │ ██   ██   ██          ▓▓          ▓▓
       │ ██   ██   ██          ▓▓          ▓▓
   5   │ ██   ██   ██          ▓▓          ▓▓
       │ ██   ██   ██          ▓▓          ▓▓
   0   └────────────────────────────────────────
        S1    S2    S3         S4          S5
                             (plan.)     (plan.)

██ = Pontos entregues     ▓▓ = Pontos planejados
```

| Sprint   | Período               | Planejados | Entregues | Velocidade |
|----------|-----------------------|------------|-----------|------------|
| Sprint 1 | 15/05 – 28/05         | 18         | 18        | 100%       |
| Sprint 2 | 29/05 – 11/06         | 30         | 30        | 100%       |
| Sprint 3 | 29/05 – 12/06         | 22         | 22        | 100%       |
| Sprint 4 | 13/06 – 26/06         | 22         | —         | *(planejada)* |
| Sprint 5 | 27/06 – 10/07         | 21         | —         | *(planejada)* |

---

## Estrutura Atual do Projeto (v2.5)

```
ProjetoFinal_LER/
├── ProjetoFinal.py          # Classe principal EduGrade — 479 linhas, 9 opções de menu
├── prototip.py              # Protótipo simplificado zero-dependências — 138 linhas
├── README.md                # Documentação completa v2.5 — 333 linhas
├── requirements.txt         # Dependências (apenas stdlib Python)
│
├── dados/
│   └── alunos.json          # Banco de dados JSON dos alunos
│
├── models/
│   ├── __init__.py           # Exports: Aluno, Disciplina
│   ├── aluno.py              # Dataclass Aluno — 84 linhas
│   └── disciplina.py         # Dataclass Disciplina — 85 linhas
│
├── services/
│   ├── __init__.py           # Exports: Calculadora, GeradorBoletim, Persistencia
│   ├── calculadora.py        # Regras de negócio RN-01 a RN-03 — 105 linhas
│   ├── boletim.py            # Gerador de boletim ASCII — 163 linhas
│   └── persistencia.py       # CRUD JSON — 83 linhas
│
└── utils/
    ├── __init__.py           # Export: Validadores
    └── validadores.py        # 6 métodos de validação — 121 linhas
```

**Total de linhas de código:** ~1.145 linhas (sem contar `__init__.py`)

---

## Impedimentos e Riscos

| # | Impedimento / Risco                                                     | Impacto         | Status         |
|---|-------------------------------------------------------------------------|-----------------|----------------|
| 1 | Encoding UTF-8 vs cp1252 no terminal Windows (caracteres box-drawing)   | Visual/Boletim  | ⚠️ Mitigado    |
| 2 | Ausência de testes automatizados (pytest/unittest)                      | Qualidade       | 📋 Sprint 4    |
| 3 | Busca de aluno somente por matrícula (não por nome)                     | Usabilidade     | 📋 Sprint 4    |
| 4 | Sem funcionalidade de edição de dados cadastrados                       | Usabilidade     | 📋 Sprint 4    |
| 5 | Dependência de biblioteca externa para exportação PDF                   | Dependência     | 📋 Sprint 5    |

---

## Métricas do Projeto

| Métrica                                | Valor              |
|----------------------------------------|--------------------|
| Total de User Stories no backlog       | 46                 |
| User Stories concluídas (v2.5)         | 32                 |
| % de conclusão                         | 69.6%              |
| Total de pontos no backlog             | 128                |
| Pontos entregues                       | 70                 |
| Velocidade média (por sprint)          | ~23 pontos         |
| Sprints concluídas                     | 3                  |
| Próxima sprint                         | Sprint 4           |
| Arquivos de código                     | 9 arquivos .py     |
| Total de linhas de código              | ~1.145 linhas      |
| Responsáveis                           | Kauan, Luis        |
