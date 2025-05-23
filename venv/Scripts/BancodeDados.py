import pandas as pd
import sqlite3
import os

# Caminho da pasta com os arquivos tratados
pasta_dados = "dados_embrapa"

# Conectar ao novo banco SQLite
conn = sqlite3.connect("vitibrasil2.db")
cursor = conn.cursor()

# Função para limpar o nome da tabela
def nome_tabela(nome_arquivo):
    return os.path.splitext(nome_arquivo)[0].lower()

# Percorre todos os arquivos da pasta
for arquivo in os.listdir(pasta_dados):
    caminho = os.path.join(pasta_dados, arquivo)

    # Define nome da tabela com base no nome do arquivo
    tabela = nome_tabela(arquivo)

    try:
        if arquivo.endswith(".xlsx"):
            df = pd.read_excel(caminho)
        elif arquivo.endswith(".csv"):
            df = pd.read_csv(caminho, sep="\t", on_bad_lines="skip")
        else:
            print(f"❌ Tipo de arquivo não suportado: {arquivo}")
            continue

        # Substitui espaços por "_" nos nomes das colunas e remove colunas vazias
        df.columns = [col.strip().replace(" ", "_") for col in df.columns if col.strip() != ""]

        # Salva os dados no banco
        df.to_sql(tabela, conn, if_exists="replace", index=False)
        print(f"✅ Dados inseridos na tabela: {tabela}")

    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {e}")

# Fecha a conexão com o banco
conn.close()
print("🎉 Banco vitibrasil2.db criado com sucesso!")
