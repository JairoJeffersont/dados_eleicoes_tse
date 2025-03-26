import os
import pandas as pd

def gerar_csv(nome_pasta):
    # Verifique se a pasta existe, senão, crie
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)

    # Crie a pasta 'csv' dentro da pasta 'nome_pasta' se ela não existir
    pasta_csv = os.path.join(nome_pasta, 'votacao_nominal')
    if not os.path.exists(pasta_csv):
        os.makedirs(pasta_csv)

    # Lista todos os arquivos CSV na pasta
    arquivos_csv = [f for f in os.listdir(nome_pasta) if f.endswith('.csv')]

    for arquivo_csv in arquivos_csv:
        # Caminho completo do arquivo CSV
        caminho_arquivo = os.path.join(nome_pasta, arquivo_csv)

        # Leia o CSV com pandas
        df = pd.read_csv(caminho_arquivo, delimiter=';', encoding='ISO-8859-1')

        # Verifica se a coluna 'QT_VOTOS_NOMINAIS_VALIDOS' existe
        if 'QT_VOTOS_NOMINAIS_VALIDOS' in df.columns:
            coluna_votos = 'QT_VOTOS_NOMINAIS_VALIDOS'
        elif 'QT_VOTOS_NOMINAIS' in df.columns:
            coluna_votos = 'QT_VOTOS_NOMINAIS'
        else:
            print(f"Erro: Nenhuma das colunas esperadas ('QT_VOTOS_NOMINAIS_VALIDOS' ou 'QT_VOTOS_NOMINAIS') foi encontrada no arquivo: {arquivo_csv}")
            continue  # Pula para o próximo arquivo

        # Agrupe por 'NM_CANDIDATO', 'NM_MUNICIPIO' e 'DS_CARGO', somando os votos
        df_agrupado = df.groupby(['NM_URNA_CANDIDATO', 'NM_MUNICIPIO', 'DS_CARGO'])[coluna_votos].sum().reset_index()

        # Agora, garantimos que a coluna de votos seja 'QT_VOTOS_NOMINAIS_VALIDOS'
        df_agrupado = df_agrupado.rename(columns={coluna_votos: 'QT_VOTOS_NOMINAIS_VALIDOS'})

        # Defina o novo caminho do arquivo dentro da pasta 'csv'
        novo_caminho_arquivo = os.path.join(pasta_csv, arquivo_csv)
        
        # Salvar o DataFrame agrupado em um novo CSV com nome modificado
        df_agrupado.to_csv(novo_caminho_arquivo, index=False, sep=';', encoding='ISO-8859-1')

        print(f'O CSV com os votos nominais foi criado com sucesso: {novo_caminho_arquivo}')
