# 📋 Product Backlog — EduGrade

**Produto:** EduGrade — Sistema de Gestão de Notas Escolares  
**Product Owner:** Kauan Andrade, Luis Otavio  
**Última atualização:** 12/06/2026  
**Versão:** 2.5  

---

## Legenda de Prioridade (MoSCoW)

| Prioridade     | Significado                                                   |
|----------------|---------------------------------------------------------------|
| 🔴 **Must**    | Indispensável — o sistema não funciona sem isso               |
| 🟠 **Should**  | Importante — agrega muito valor, mas não bloqueia o uso       |
| 🟡 **Could**   | Desejável — melhoria de experiência, pode ficar para depois   |
| ⚪ **Won't**   | Não será feito agora — backlog futuro                         |

## Legenda de Status

| Status            | Significado                        |
|-------------------|------------------------------------|
| ✅ Concluído      | Implementado e testado             |
| 📋 A Fazer        | Priorizado, aguardando sprint      |
| 💤 Futuro         | Baixa prioridade / versão futura   |

---

## Épico 1 — Cadastro e Gerenciamento de Alunos

> **Objetivo:** Permitir que o professor cadastre, liste e remova alunos no sistema.
>
> **Arquivos envolvidos:** `ProjetoFinal.py`, `models/aluno.py`, `services/persistencia.py`, `utils/validadores.py`

| ID     | User Story                                                                                                                                              | Prioridade   | Pontos | Status        |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------|---------------|
| US-01  | Como professor, quero **cadastrar um aluno** com nome e matrícula para registrá-lo no sistema.                                                          | 🔴 Must      | 3      | ✅ Concluído  |
| US-02  | Como professor, quero que a **matrícula seja única** para evitar duplicidade de cadastro.                                                                | 🔴 Must      | 2      | ✅ Concluído  |
| US-03  | Como professor, quero **listar todos os alunos** cadastrados para ter visão geral da turma.                                                             | 🔴 Must      | 2      | ✅ Concluído  |
| US-04  | Como professor, quero **remover um aluno** por matrícula para excluir cadastros incorretos ou inativos.                                                 | 🟠 Should    | 3      | ✅ Concluído  |

### Critérios de Aceitação — US-01 (Implementados)
- O sistema solicita matrícula e nome via terminal (`ler_string`).
- Matrícula aceita apenas caracteres alfanuméricos (`validar_matricula` → `isalnum`).
- Nome deve ter pelo menos 2 caracteres (`validar_nome`).
- Matrícula duplicada é rejeitada com mensagem `"Já existe um aluno com a matrícula"`.
- Após cadastro, os dados são salvos no `dados/alunos.json` automaticamente.

### Critérios de Aceitação — US-04 (Implementados)
- O sistema exibe resumo do aluno (nome, matrícula, quantidade de disciplinas) antes da exclusão.
- Confirmação (s/n) é obrigatória antes de remover.
- Todos os dados do aluno (disciplinas, notas, frequência) são removidos em cascata.
- JSON é regravado após remoção.

---

## Épico 2 — Gerenciamento de Disciplinas

> **Objetivo:** Permitir o cadastro e remoção de disciplinas associadas a alunos.
>
> **Arquivos envolvidos:** `ProjetoFinal.py`, `models/aluno.py`, `models/disciplina.py`

| ID     | User Story                                                                                                                               | Prioridade   | Pontos | Status        |
|--------|------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------|---------------|
| US-07  | Como professor, quero **cadastrar disciplinas** para um aluno para organizar suas matérias.                                              | 🔴 Must      | 3      | ✅ Concluído  |
| US-08  | Como professor, quero que o sistema **impeça disciplinas duplicadas** no mesmo aluno.                                                    | 🔴 Must      | 2      | ✅ Concluído  |
| US-09  | Como professor, quero **remover uma disciplina** de um aluno para corrigir erros de cadastro.                                            | 🟠 Should    | 3      | ✅ Concluído  |
| US-10  | Como professor, quero **visualizar as disciplinas** de um aluno ao selecioná-lo para saber em quais ele está matriculado.                | 🟠 Should    | 2      | ✅ Concluído  |

### Critérios de Aceitação — US-08 (Implementados)
- O método `aluno.adicionar_disciplina()` compara nomes com `lower()` (case-insensitive).
- Se já existir, lança `ValueError` com a mensagem `"Aluno 'X' já está matriculado em 'Y'"`.

### Critérios de Aceitação — US-09 (Implementados)
- O sistema lista as disciplinas numeradas para seleção visual.
- Confirmação (s/n) é obrigatória antes de remover.
- As notas e frequência associadas à disciplina são removidas junto com o objeto.

---

## Épico 3 — Registro de Notas

> **Objetivo:** Permitir o registro e cálculo de notas dos alunos por disciplina.
>
> **Arquivos envolvidos:** `ProjetoFinal.py`, `models/disciplina.py`, `services/calculadora.py`, `utils/validadores.py`

| ID     | User Story                                                                                                                               | Prioridade   | Pontos | Status        |
|--------|------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------|---------------|
| US-12  | Como professor, quero **registrar 3 notas** (N1, N2, N3) por disciplina para cada aluno.                                                | 🔴 Must      | 5      | ✅ Concluído  |
| US-13  | Como professor, quero que as notas sejam **validadas entre 0.0 e 10.0** para evitar dados incorretos.                                   | 🔴 Must      | 2      | ✅ Concluído  |
| US-14  | Como professor, quero **substituir notas já registradas** caso tenha cometido erro de digitação.                                         | 🟠 Should    | 3      | ✅ Concluído  |
| US-15  | Como professor, quero que o sistema exiba a **média imediatamente** após registrar as 3 notas.                                           | 🟠 Should    | 1      | ✅ Concluído  |
| US-16  | Como coordenador, quero poder registrar **notas com pesos diferentes** (média ponderada) para disciplinas especiais.                     | ⚪ Won't     | 5      | 💤 Futuro     |

### Critérios de Aceitação — US-12 (Implementados)
- O sistema solicita exatamente 3 notas em loop (`range(3)`).
- Cada nota é validada por `ler_float(minimo=0.0, maximo=10.0)`.
- Após registro, `Calculadora.calcular_media()` é chamado e a média é exibida com 2 casas decimais.
- Os dados são salvos automaticamente no `alunos.json`.

### Critérios de Aceitação — US-14 (Implementados)
- Se `disciplina.notas_completas` é `True` (já tem 3 notas), pergunta "Deseja substituir? (s/n)".
- Se confirmado, as notas anteriores são apagadas com `disciplina.notas.clear()`.

---

## Épico 4 — Controle de Frequência

> **Objetivo:** Registrar e verificar a frequência mínima obrigatória dos alunos.
>
> **Arquivos envolvidos:** `ProjetoFinal.py`, `models/disciplina.py`, `services/calculadora.py`, `utils/validadores.py`

| ID     | User Story                                                                                                                                  | Prioridade   | Pontos | Status        |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------|---------------|
| US-17  | Como professor, quero **registrar a frequência** (aulas assistidas / total) de um aluno por disciplina.                                     | 🔴 Must      | 3      | ✅ Concluído  |
| US-18  | Como professor, quero que o sistema **valide** que aulas assistidas ≤ total de aulas.                                                       | 🔴 Must      | 2      | ✅ Concluído  |
| US-19  | Como professor, quero ver **imediatamente se a frequência está abaixo de 75%** ao registrá-la para tomar providências.                      | 🟠 Should    | 1      | ✅ Concluído  |
| US-20  | Como professor, quero poder **registrar presença aula a aula** em vez de inserir o total de uma vez.                                        | ⚪ Won't     | 8      | 💤 Futuro     |

### Critérios de Aceitação — US-17 (Implementados)
- O sistema solicita total de aulas (`ler_int(minimo=1)`) e aulas assistidas (`ler_int(minimo=0, maximo=total_aulas)`).
- O percentual de frequência é calculado por `Calculadora.calcular_frequencia()`.
- Exibe alerta visual: `"✅ Dentro do mínimo"` ou `"❌ Abaixo do mínimo (75%)"`.

---

## Épico 5 — Lógica de Aprovação e Status

> **Objetivo:** Determinar automaticamente o status do aluno com base nas regras de negócio (RN-01 a RN-03).
>
> **Arquivos envolvidos:** `services/calculadora.py` (classe `Calculadora` e `Status`)

| ID     | User Story                                                                                                                                       | Prioridade   | Pontos | Status        |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------|---------------|
| US-21  | Como professor, quero que o sistema calcule a **média aritmética** automaticamente: `(N1+N2+N3)/3`.                                              | 🔴 Must      | 2      | ✅ Concluído  |
| US-22  | Como professor, quero que o aluno seja **aprovado** se média ≥ 7.0 e frequência ≥ 75%.                                                           | 🔴 Must      | 3      | ✅ Concluído  |
| US-23  | Como professor, quero que o aluno vá para **recuperação** se média entre 5.0 e 6.9 e frequência ≥ 75%.                                            | 🔴 Must      | 3      | ✅ Concluído  |
| US-24  | Como professor, quero que o aluno seja **reprovado direto** se média < 5.0.                                                                       | 🔴 Must      | 2      | ✅ Concluído  |
| US-25  | Como professor, quero que o aluno seja **reprovado por falta** se frequência < 75%, independente da nota.                                          | 🔴 Must      | 3      | ✅ Concluído  |
| US-26  | Como coordenador, quero **consultar o status** de um aluno em uma disciplina específica em formato detalhado.                                     | 🟠 Should    | 2      | ✅ Concluído  |
| US-27  | Como professor, quero que a **frequência seja verificada antes da média** (prioridade de frequência conforme RN-03).                               | 🔴 Must      | 2      | ✅ Concluído  |
| US-28  | Como professor, quero que o sistema registre **nota de recuperação** para alunos em recuperação e recalcule o status final.                        | ⚪ Won't    | 5      | 💤 Futuro  |

### Critérios de Aceitação — US-25 (Implementados)
- `Calculadora.determinar_status()` verifica `frequencia < FREQUENCIA_MINIMA (75.0)` **antes** da média.
- Se frequência < 75%, retorna `Status.REPROVADO_FALTA` independentemente da média.
- Validado no teste: média 10.0 com frequência 50% → "REPROVADO POR FALTA".

---

## Épico 6 — Boletim Final

> **Objetivo:** Gerar relatório consolidado com notas, frequência e status de cada disciplina.
>
> **Arquivos envolvidos:** `services/boletim.py` (classe `GeradorBoletim`)

| ID     | User Story                                                                                                                               | Prioridade   | Pontos | Status        |
|--------|------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------|---------------|
| US-29  | Como coordenador, quero **gerar o boletim final** de um aluno com todas as disciplinas.                                                  | 🔴 Must      | 5      | ✅ Concluído  |
| US-30  | Como coordenador, quero que o boletim mostre **N1, N2, N3, média, frequência e status** por disciplina em tabela formatada.               | 🔴 Must      | 3      | ✅ Concluído  |
| US-31  | Como coordenador, quero ver um **resumo** com contagem de aprovações, recuperações e reprovações no final do boletim.                    | 🟠 Should    | 2      | ✅ Concluído  |
| US-32  | Como coordenador, quero **exportar o boletim em PDF** para impressão e arquivamento.                                                     | ⚪ Won't     | 8      | 💤 Futuro     |
| US-33  | Como coordenador, quero **exportar o boletim em CSV** para análise em planilhas.                                                         | ⚪ Won't     | 5      | 💤 Futuro     |

### Critérios de Aceitação — US-29 (Implementados)
- O boletim é renderizado como tabela ASCII com box-drawing characters (`╔═║─┼`).
- Cabeçalho com nome e matrícula do aluno.
- Colunas: Disciplina (16 chars), N1, N2, N3, Média, Frequência, Status (abreviado).
- Legenda de abreviações (APROV., RECUP., REPROV., R.FALTA) no rodapé.
- Resumo estatístico com `_gerar_resumo()` contando aprovados, recuperação, reprovados e incompletos.

---

## Épico 7 — Persistência de Dados

> **Objetivo:** Salvar e recuperar dados entre sessões do sistema.
>
> **Arquivos envolvidos:** `services/persistencia.py`, `dados/alunos.json`

| ID     | User Story                                                                                                                               | Prioridade   | Pontos | Status        |
|--------|------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------|---------------|
| US-34  | Como professor, quero que meus dados sejam **salvos automaticamente** em `dados/alunos.json` a cada operação.                            | 🔴 Must      | 3      | ✅ Concluído  |
| US-35  | Como professor, quero que os dados sejam **carregados automaticamente ao abrir** o sistema.                                              | 🔴 Must      | 2      | ✅ Concluído  |
| US-36  | Como professor, quero que o sistema **trate erros** graciosamente se o arquivo JSON estiver corrompido, iniciando com lista vazia.        | 🟠 Should    | 3      | ✅ Concluído  |
| US-37  | Como administrador, quero poder **migrar para banco de dados SQLite** no futuro para suportar mais dados.                                | ⚪ Won't     | 13     | 💤 Futuro     |

### Critérios de Aceitação — US-36 (Implementados)
- `Persistencia.carregar()` captura `json.JSONDecodeError` e `KeyError`.
- Exibe `"⚠️ Erro ao carregar dados"` e inicia com lista vazia sem travar o sistema.
- O diretório `dados/` é criado automaticamente com `os.makedirs(exist_ok=True)`.

---

## Épico 8 — Melhorias Futuras

> **Objetivo:** Funcionalidades desejáveis para versões futuras do sistema.

| ID     | User Story                                                                                                                               | Prioridade   | Pontos | Status        |
|--------|------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------|---------------|
| US-42  | Como coordenador, quero uma **interface gráfica (GUI)** para facilitar o uso por usuários não-técnicos.                                  | ⚪ Won't     | 21     | 💤 Futuro     |
| US-43  | Como coordenador, quero **relatórios por turma** para visão geral de uma classe inteira.                                                 | ⚪ Won't      | 8      | 💤 Futuro    |
| US-44  | Como coordenador, quero **gráficos de desempenho** do aluno ao longo do tempo.                                                           | ⚪ Won't     | 13     | 💤 Futuro     |
| US-45  | Como coordenador, quero suporte a **múltiplos períodos letivos** (bimestres/semestres).                                                  | ⚪ Won't     | 13     | 💤 Futuro     |
| US-46  | Como administrador, quero **login com senha** para proteger os dados dos alunos.                                                         | ⚪ Won't      | 8      | 💤 Futuro    |

---

## Resumo do Product Backlog

| Prioridade     | Total | Concluídas | A Fazer | Futuro |
|----------------|-------|------------|---------|--------|
| 🔴 Must        | 19    | 19         | 0       | 0      |
| 🟠 Should      | 9     | 9          | 0       | 0      |
| 🟡 Could       | 0     | 0          | 0       | 0      |
| ⚪ Won't       | 11    | 0          | 0       | 11     |
| **Total**      | **39**| **28**     | **0**   | **11** |

---

## Rastreabilidade — User Stories × Arquivos

| Arquivo                        | User Stories Relacionadas                            |
|--------------------------------|------------------------------------------------------|
| `ProjetoFinal.py`              | US-01 a US-04, US-07 a US-10, US-12 a US-16, US-17 a US-20 |
| `models/aluno.py`              | US-01, US-02, US-04, US-07, US-08, US-34, US-35      |
| `models/disciplina.py`         | US-07 a US-10, US-12 a US-16, US-17 a US-20          |
| `services/calculadora.py`      | US-21 a US-28                                         |
| `services/boletim.py`          | US-29 a US-33                                         |
| `services/persistencia.py`     | US-34, US-35, US-36                                   |
| `utils/validadores.py`         | US-01, US-02, US-13, US-18                            |
| `dados/alunos.json`            | US-34, US-35, US-36                                   |

---

> **Velocity média:** ~20 pontos por sprint (sprints de 2 semanas)  
> **Total de pontos entregues (v2.5):** 72 pontos  
> **Total de pontos restantes no backlog:** 56 pontos
