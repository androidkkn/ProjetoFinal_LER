# prototip.py
# Protótipo do sistema EduGrade
    
alunos = []

def cadastrar_aluno(matricula, nome):
    """Cadastra um novo aluno se a matrícula não existir."""
    for aluno in alunos:
        if aluno['matricula'] == matricula:
            print("❌ Matrícula já cadastrada.")
            return
    
    alunos.append({
        'matricula': matricula,
        'nome': nome,
        'notas': [],
        'aulas_total': 0,
        'aulas_assistidas': 0
    })
    print(f"✅ Aluno {nome} cadastrado com sucesso.")

def registrar_notas(matricula, n1, n2, n3):
    """Registra 3 notas para o aluno correspondente."""
    for aluno in alunos:
        if aluno['matricula'] == matricula:
            aluno['notas'] = [n1, n2, n3]
            print(f"✅ Notas registradas para {aluno['nome']}.")
            return
    print("❌ Aluno não encontrado.")

def registrar_frequencia(matricula, assistidas, total):
    """Registra a frequência de um aluno."""
    if total <= 0 or assistidas < 0 or assistidas > total:
        print("❌ Dados de frequência inválidos.")
        return
        
    for aluno in alunos:
        if aluno['matricula'] == matricula:
            aluno['aulas_assistidas'] = assistidas
            aluno['aulas_total'] = total
            print(f"✅ Frequência registrada para {aluno['nome']}.")
            return
    print("❌ Aluno não encontrado.")

def calcular_status(aluno):
    """Calcula e retorna o status do aluno baseado nas regras de negócio."""
    if aluno['aulas_total'] == 0:
        return "Dados Incompletos (Frequência)"
    
    frequencia = (aluno['aulas_assistidas'] / aluno['aulas_total']) * 100
    
    # Prioridade para frequência
    if frequencia < 75.0:
        return "Reprovado por Falta"
        
    if not aluno['notas'] or len(aluno['notas']) < 3:
        return "Dados Incompletos (Notas)"
        
    media = sum(aluno['notas']) / 3
    
    if media >= 7.0:
        return "Aprovado"
    elif media >= 5.0:
        return "Recuperação"
    else:
        return "Reprovado Direto"

def exibir_boletins():
    """Exibe os boletins simplificados de todos os alunos."""
    if not alunos:
        print("⚠️ Nenhum aluno cadastrado.")
        return
        
    print("\n--- 📋 BOLETINS ---")
    for aluno in alunos:
        status = calcular_status(aluno)
        
        media = sum(aluno['notas']) / 3 if len(aluno['notas']) == 3 else 0.0
        freq = (aluno['aulas_assistidas'] / aluno['aulas_total']) * 100 if aluno['aulas_total'] > 0 else 0.0
        
        print(f"Aluno: {aluno['nome']} (Matrícula: {aluno['matricula']})")
        print(f"Média: {media:.2f} | Frequência: {freq:.1f}%")
        print(f"Status: {status}")
        print("-" * 25)

def menu():
    """Loop principal de interação via terminal."""
    while True:
        print("\n--- 🎓 EduGrade (Protótipo Simplificado) ---")
        print("1. Cadastrar Aluno")
        print("2. Registrar Notas")
        print("3. Registrar Frequência")
        print("4. Exibir Boletins")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            matricula = input("Matrícula: ")
            nome = input("Nome: ")
            cadastrar_aluno(matricula, nome)
            
        elif opcao == "2":
            matricula = input("Matrícula: ")
            try:
                n1 = float(input("Nota 1 (0-10): "))
                n2 = float(input("Nota 2 (0-10): "))
                n3 = float(input("Nota 3 (0-10): "))
                if all(0 <= n <= 10 for n in [n1, n2, n3]):
                    registrar_notas(matricula, n1, n2, n3)
                else:
                    print("❌ Notas devem estar entre 0 e 10.")
            except ValueError:
                print("❌ Valor numérico inválido.")
                
        elif opcao == "3":
            matricula = input("Matrícula: ")
            try:
                total = int(input("Total de aulas: "))
                assistidas = int(input("Aulas assistidas: "))
                registrar_frequencia(matricula, assistidas, total)
            except ValueError:
                print("❌ Valor numérico inválido.")
                
        elif opcao == "4":
            exibir_boletins()
            
        elif opcao == "0":
            print("Saindo...")
            break
            
        else:
            print("❌ Opção inválida.")

# Ponto de entrada
if __name__ == "__main__":
    menu()
