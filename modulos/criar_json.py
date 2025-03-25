import os
import pandas as pd
import json
import gzip
import unicodedata

def remover_caracteres_especiais(texto):
    # Remove acentos e caracteres especiais
    return ''.join(
        (c for c in unicodedata.normalize('NFD', texto)
         if unicodedata.category(c) != 'Mn')
    )

def csvs_to_json(pasta, colunas):
    print('Criando arquivos JSON...')
    
    # Obtém o nome da pasta original para criar o diretório de saída
    nome_pasta_original = os.path.basename(pasta)
    diretorio_saida = os.path.join('json', nome_pasta_original)
    
    # Cria o diretório de saída se não existir
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
    
    # Percorre todos os arquivos na pasta
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".csv"):
            caminho_arquivo = os.path.join(pasta, arquivo)
            nome_arquivo_json = os.path.splitext(arquivo)[0] + '.jsonl.gz'  # Nome do arquivo JSONL
            caminho_saida_json = os.path.join(diretorio_saida, nome_arquivo_json)
            
            try:
                # Lê o arquivo CSV com o delimitador correto ";", e a codificação apropriada
                df = pd.read_csv(caminho_arquivo, sep=';', encoding='ISO-8859-1')
                
                # Verifica se as colunas solicitadas existem no arquivo CSV
                colunas_existentes = [coluna for coluna in colunas if coluna in df.columns]
                
                # Aplica a remoção de caracteres especiais nas colunas existentes
                for coluna in colunas_existentes:
                    df[coluna] = df[coluna].apply(lambda x: remover_caracteres_especiais(str(x)))
                
                # Converte os dados para um formato JSONL
                dados = df[colunas_existentes].to_dict(orient='records')
                
                # Salva os dados no arquivo JSONL compactado
                with gzip.open(caminho_saida_json, "wt", encoding='utf-8') as f:
                    for registro in dados:
                        json.dump(registro, f, ensure_ascii=False)
                        f.write('\n')  # Cada objeto JSON em uma linha

                print(f"JSONL comprimido salvo em: {caminho_saida_json}")
            except Exception as e:
                print(f"Erro ao ler o arquivo {arquivo}: {e}")


