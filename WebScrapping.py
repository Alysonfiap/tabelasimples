import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from concurrent.futures import ThreadPoolExecutor

# Conecta ao banco
conn = sqlite3.connect("vitibrasil.db")

# Função para limpar nomes de colunas
def limpar_colunas(df):
    df.columns = [
        col.strip()
           .lower()
           .replace(" ", "_")
           .replace(".", "")
           .replace("(", "")
           .replace(")", "")
        for col in df.columns
    ]
    return df

# -------- Produção e Comercialização (sem subopção) --------
def pegar_tabela(ano, opcao):
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tabela = soup.find('table', class_='tb_base tb_dados')

    if not tabela:
        return None

    linhas = tabela.find_all('tr')
    dados = []
    for i, linha in enumerate(linhas):
        colunas = linha.find_all(['th', 'td'])
        texto = [col.get_text(strip=True) for col in colunas]
        if texto:
            dados.append([ano, opcao] + texto if i != 0 else ['ano', 'opcao'] + texto)
    return dados

def coletar_sem_subopcao(opcao, nome_tabela):
    anos = range(1970, 2025)
    parametros = [(ano, opcao) for ano in anos]

    with ThreadPoolExecutor(max_workers=10) as executor:
        resultados = list(executor.map(lambda p: pegar_tabela(*p), parametros))

    dfs = []
    for resultado in resultados:
        if resultado:
            df = pd.DataFrame(resultado[1:], columns=resultado[0])
            df = limpar_colunas(df)
            dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)
    df_final.to_sql(nome_tabela, conn, if_exists="replace", index=False)
    print(f"✅ Tabela {nome_tabela} inserida no banco com sucesso.")

# -------- Com subopção --------
def pegar_tabela_com_subopcao(ano, opcao, subopcao):
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}&subopcao={subopcao}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tabela = soup.find('table', class_='tb_base tb_dados')

    if not tabela:
        return None

    linhas = tabela.find_all('tr')
    dados = []
    for i, linha in enumerate(linhas):
        colunas = linha.find_all(['th', 'td'])
        texto = [col.get_text(strip=True) for col in colunas]
        if texto:
            dados.append([ano, opcao, subopcao] + texto if i != 0 else ['ano', 'opcao', 'subopcao'] + texto)
    return dados

def coletar_com_subopcao(opcao, subopcoes, nome_tabela):
    anos = range(1970, 2025)
    parametros = [(ano, opcao, subop) for ano in anos for subop in subopcoes]

    with ThreadPoolExecutor(max_workers=10) as executor:
        resultados = list(executor.map(lambda p: pegar_tabela_com_subopcao(*p), parametros))

    dfs = []
    for resultado in resultados:
        if resultado:
            df = pd.DataFrame(resultado[1:], columns=resultado[0])
            df = limpar_colunas(df)
            dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)
    df_final.to_sql(nome_tabela, conn, if_exists="replace", index=False)
    print(f"✅ Tabela {nome_tabela} inserida no banco com sucesso.")

# -------- Execução --------
if __name__ == "__main__":
    # Sem subopções
    coletar_sem_subopcao('opt_02', 'producao')
    coletar_sem_subopcao('opt_04', 'comercializacao')

    # Com subopções
    coletar_com_subopcao('opt_03', ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04'], 'processamento')
    coletar_com_subopcao('opt_05', ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04', 'subopt_05'], 'importacao')
    coletar_com_subopcao('opt_06', ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04'], 'exportacao')