import pandas as pd
import os

# Caminho para o arquivo TSV
caminho_tsv = "dados_embrapa/ProcessaAmericanas.tsv"

# Caminho para salvar o novo Excel
caminho_excel = "dados_embrapa/ProcessaAmericanas.xlsx"

# Ler o arquivo com separador por tabulação
df = pd.read_csv(caminho_tsv, sep='\t', on_bad_lines='skip')

# (Opcional) Tratamento simples de exemplo: remover linhas totalmente vazias
df.dropna(how='all', inplace=True)

# Salvar em Excel substituindo o anterior
df.to_excel(caminho_excel, index=False)

print(f"Arquivo tratado e salvo em: {caminho_excel}")
