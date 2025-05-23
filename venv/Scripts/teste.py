import sqlite3
import pandas as pd

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('vitibrasil.db')

# Escreva sua consulta SQL aqui
query = """
SELECT * FROM comercio WHERE Produto LIKE '%Tinto%' ;
"""

# Executar e carregar o resultado em um DataFrame
df_resultado = pd.read_sql_query(query, conn)

# Exibir os dados
print(df_resultado)

# Fechar a conexão
conn.close()
