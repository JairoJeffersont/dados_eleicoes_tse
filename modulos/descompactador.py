import zipfile
import os

def descompactar_arquivo(zip_path, pasta_destino):
    # Verificar se o arquivo ZIP existe
    if not os.path.exists(zip_path):
        print(f"Arquivo {zip_path} não encontrado.")
        return

    # Verificar se a pasta de destino existe, se não, criar
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    try:
        # Abrir o arquivo ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extrair todos os arquivos para a pasta de destino
            zip_ref.extractall(pasta_destino)
            print(f"Arquivos descompactados em: {pasta_destino}\n")
    
    except zipfile.BadZipFile:
        print(f"O arquivo {zip_path} não é um arquivo ZIP válido.")
    except Exception as e:
        print(f"Erro ao descompactar o arquivo: {e}")


