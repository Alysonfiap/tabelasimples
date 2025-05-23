import sqlite3

conn = sqlite3.connect("vitibrasil_opt03.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM dados_opt03")
for linha in cursor.fetchall():
    print(linha)

conn.close()
