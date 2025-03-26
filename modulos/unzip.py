import zipfile
import os

def unzip(zip_path):
    if zipfile.is_zipfile(zip_path):
        pasta_destino = os.path.dirname(zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(pasta_destino)
        
        os.remove(zip_path)
        print(f'Arquivo {zip_path} descompactado e excluído com sucesso!\n')
    else:
        print(f'O arquivo {zip_path} não é um arquivo ZIP válido.')


