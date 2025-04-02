from .app import MergulhoEmailer

def main():
    """Função principal que inicia a aplicação"""
    app = MergulhoEmailer()
    success = app.run()
    
    if success:
        print("Processo concluído com sucesso!")
    else:
        print("Erro ao executar o processo.")
        exit(1)

if __name__ == "__main__":
    main() 