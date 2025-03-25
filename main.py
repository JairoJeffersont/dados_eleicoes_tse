import os
from modulos import downloader
from modulos import criar_json


# Função genérica para baixar e descompactar arquivos
def baixar(ano):
    print(f'Iniciando o download dos arquivos da eleição de {ano}....')
    downloader.download_arquivo(ano, f"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_{ano}.zip")
    downloader.download_arquivo(ano, f"https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_munzona/detalhe_votacao_munzona_{ano}.zip")
    downloader.download_arquivo(ano, f"https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_secao/detalhe_votacao_secao_{ano}.zip")
    
# Corrigindo a função baixar_tudo
def baixar_tudo(ultima_eleicao):
    for ano in range(2000, ultima_eleicao + 1, 2):
        baixar(ano)

# Função principal do menu
def menu():
    while True:
        
        print("\n--- MENU ---")
        print("1. Baixar os arquivos de uma eleição específica")
        print("2. Baixar os arquivos de todas as eleições")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            ano = int(input("Digite o ano da eleição: "))
            baixar(ano)
        elif opcao == "2":
            ultima_eleicao = int(input("Digite o ano da última eleição: "))
            baixar_tudo(ultima_eleicao)    
        elif opcao == "4":
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
