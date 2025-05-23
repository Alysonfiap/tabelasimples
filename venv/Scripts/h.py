from bs4 import BeautifulSoup
import pandas as pd 

# Abre o arquivo HTML salvo
with open("pagina_opt03.html", "r", encoding="utf-8") as f:
    conteudo_html = f.read()

# Agora sim, passe o conteúdo para o BeautifulSoup
soup = BeautifulSoup(conteudo_html, "html.parser")


# Localiza a tabela com as classes específicas
tabela = soup.find("table", class_="tb_base tb_dados")


tabelas = pd.read_html(str(tabela))  # Converte a tag para string


# Mostra a primeira tabela encontrada (ou escolha o índice correto se houver mais de uma)
df = tabelas[0]

print(df)

