import requests
import os
import time

def download_arquivo(url, pasta_destino, tentativas_max=3, intervalo_tentativas=5):
    print(f"\nIniciando download....\n")
    
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    tentativas = 0
    while tentativas < tentativas_max:
        try:
            resposta = requests.get(url, stream=True)
            resposta.raise_for_status()
            break
        except (requests.RequestException, requests.ConnectionError) as erro:
            tentativas += 1
            print(f"Erro ao acessar a URL: {erro}. Tentando novamente em {intervalo_tentativas} segundos... ({tentativas}/{tentativas_max})")
            time.sleep(intervalo_tentativas)
            if tentativas == tentativas_max:
                print("Número máximo de tentativas atingido. O download falhou.")
                return
    
    tamanho_total = resposta.headers.get('content-length')
    tamanho_total = int(tamanho_total) if tamanho_total else None
    nome_arquivo = os.path.join(pasta_destino, url.split('/')[-1])
    
    baixado = 0
    tamanho_mb = (tamanho_total / (1024 * 1024)) if tamanho_total else None
    inicio = time.time()
    
    with open(nome_arquivo, 'wb') as arquivo:
        for chunk in resposta.iter_content(chunk_size=1024 * 1024):  # 1MB
            if chunk:
                arquivo.write(chunk)
                baixado += len(chunk)
                baixado_mb = baixado / (1024 * 1024)
                tempo_decorrido = time.time() - inicio
                velocidade = baixado_mb / tempo_decorrido if tempo_decorrido > 0 else 0
                
                if tamanho_total:
                    percentual = (baixado / tamanho_total) * 100
                    # Calculando o tempo restante
                    tempo_restante = (tamanho_total - baixado) / (velocidade * 1024 * 1024) if velocidade > 0 else 0
                    minutos_restantes = int(tempo_restante // 60)
                    segundos_restantes = int(tempo_restante % 60)
                    print(f"{baixado_mb:.2f} MB de {tamanho_mb:.2f} MB ({percentual:.2f}%) - {velocidade:.2f} MB/s - Tempo restante: {minutos_restantes:02}:{segundos_restantes:02}", end='\r')
                else:
                    print(f"{baixado_mb:.2f} MB baixados - {velocidade:.2f} MB/s", end='\r')
    
    print("\n\nDownload concluído!")
    print(f"O arquivo foi salvo na pasta {pasta_destino}/{nome_arquivo}\n")
