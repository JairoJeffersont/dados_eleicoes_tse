import os
from modulos import downloader
from modulos import unzip
from modulos import csv_votos_nominal


def menu_ano():
    
    os.system("cls" if os.name == "nt" else "clear")
    
    print("🚨 Digite o ano da primeira e última eleição para baixar os arquivos dos servidores do TSE.")
    
    ano_inicial = int(input("\nAno da primeira eleição desejada: "))
    ano_final = int(input("Ano da última eleição desejada: "))
    
    for ano in range(ano_inicial, ano_final + 1, 2):
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 50)
        print(f"                ELEIÇÃO DO ANO {ano}          ")
        print("=" * 50)
        downloader.download_arquivo(f"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_{ano}.zip", f"dados_tse/{ano}")
        print("Descompactando arquivos...")
        unzip.unzip(f"dados_tse/{ano}/votacao_candidato_munzona_{ano}.zip")
        csv_votos_nominal.gerar_csv(f"dados_tse/{ano}")
    input("Pressione ENTER para continuar...")
    
    
def menu_normalizar():
    
    os.system("cls" if os.name == "nt" else "clear")

    ano_inicial = int(input("\nAno da primeira eleição desejada: "))
    ano_final = int(input("Ano da última eleição desejada: "))
    for ano in range(ano_inicial, ano_final + 1, 2):
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 50)
        print(f"                ELEIÇÃO DO ANO {ano}          ")
        print("=" * 50)
        csv_votos_nominal.gerar_csv(f"dados_tse/{ano}")
    input("Pressione ENTER para continuar...")
    

    
    
    
    

