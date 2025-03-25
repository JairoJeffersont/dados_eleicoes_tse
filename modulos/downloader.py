import os
import requests
import time

from modulos import descompactador

def download_arquivo(ano, url, tentativas_max=5, intervalo_tentativas=3):
    # Verificar se a pasta existe, se não, criar
    nome_pasta = f"zip/{ano}"
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)
    
    # Obter o nome do arquivo a partir da URL
    nome_arquivo = url.split("/")[-1]
    
    # Caminho completo onde o arquivo será salvo
    caminho_arquivo = os.path.join(nome_pasta, nome_arquivo)
    
    # Verificar se o arquivo já existe
    if os.path.exists(caminho_arquivo):
        print(f"O arquivo '{nome_arquivo}' já existe. Pulando o download.")
        descompactador.descompactar_arquivo(caminho_arquivo, f"csv/{ano}")
        return
    
    tentativa = 0
    while tentativa < tentativas_max:
        try:
            # Fazendo o download do arquivo com stream=True para poder monitorar o progresso
            resposta = requests.get(url, stream=True)
            resposta.raise_for_status()  # Levanta um erro se a resposta não for bem-sucedida
            
            # Obter o tamanho total do arquivo a partir do cabeçalho Content-Length
            tamanho_total = int(resposta.headers.get('Content-Length', 0))
            
            # Se o tamanho total for 0, não podemos calcular o progresso
            if tamanho_total == 0:
                print("Não foi possível determinar o tamanho do arquivo.")
                return
            
            # Salvar o arquivo no caminho especificado, monitorando o progresso
            with open(caminho_arquivo, 'wb') as f:
                bytes_baixados = 0
                tempo_inicial = time.time()  # Marca o início do download
                
                for dados in resposta.iter_content(chunk_size=1024):  # Baixando em pedaços de 1 KB
                    f.write(dados)
                    bytes_baixados += len(dados)
                    
                    # Calcular o tempo passado
                    tempo_passado = time.time() - tempo_inicial
                    
                    # Calcular a velocidade de download em MB/s
                    velocidade_mb_s = (bytes_baixados / (1024 * 1024)) / tempo_passado  # MB/s
                    
                    # Calcular o progresso
                    progresso = (bytes_baixados / tamanho_total) * 100
                    
                    # Exibir o progresso e a velocidade de download (em MB/s)
                    progresso_mb = bytes_baixados / (1024 * 1024)  # Converter para MB
                    tamanho_total_mb = tamanho_total / (1024 * 1024)  # Converter para MB
                    print(f"Baixando {progresso_mb:.2f} MB de {tamanho_total_mb:.2f} MB "
                          f"({progresso:.2f}%) | Velocidade: {velocidade_mb_s:.2f} MB/s", end='\r')
            
            print(f"\nArquivo salvo em: {caminho_arquivo}\n")
            descompactador.descompactar_arquivo(caminho_arquivo, f"csv/{ano}")
            return  # Se o download for bem-sucedido, sai da função
        except requests.exceptions.RequestException as e:
            tentativa += 1
            print(f"\nErro ao fazer download do arquivo (Tentativa {tentativa}/{tentativas_max}): {e}")
            if tentativa < tentativas_max:
                print(f"Esperando {intervalo_tentativas} segundos antes de tentar novamente...")
                time.sleep(intervalo_tentativas)  # Espera antes de tentar novamente
            else:
                print("Máximo de tentativas alcançado. Não foi possível baixar o arquivo.")
                return