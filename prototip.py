"""
EduGrade — Sistema de Gestão de Notas Escolares
================================================
Arquivo principal de inicialização (Entrypoint).
Este arquivo serve como o ponto de partida do sistema,
instanciando a aplicação principal e iniciando o loop do menu.
"""

import sys
from antiGTest import EduGrade

def main() -> None:
    """Função principal que inicializa e executa o sistema EduGrade."""
    try:
        # Instancia o controlador principal do sistema
        app = EduGrade()
        
        # Inicia o loop interativo do menu
        app.executar()
        
    except KeyboardInterrupt:
        # Captura o encerramento manual (Ctrl+C) de forma amigável
        print("\n\n  👋 Programa encerrado pelo usuário. Até logo!")
        sys.exit(0)

if __name__ == "__main__":
    main()
