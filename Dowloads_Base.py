import requests
import pandas as pd
import os
from io import StringIO

arquivos = [
    ("Producao.xlsx", "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"),
    ("ProcessaViniferas.xlsx", "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"),
    ("ProcessaAmericanas.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv"),
    ("ProcessaMesa.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv"),
    ("ProcessaSemclass.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv"),
    ("Comercio.xlsx", "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"),
    ("ImpVinhos.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv"),
    ("ImpEspumantes.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv"),
    ("ImpFrescas.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv"),
    ("ImpPassas.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv"),
    ("ImpSuco.xlsx", "http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv"),
    ("ExpVinho.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"),
    ("ExpEspumantes.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv"),
    ("ExpUva.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv"),
    ("ExpSuco.csv", "http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv")
]

# Lista de arquivos que devem ser tratados como TSV (tabulação)
tsv_arquivos = {
    "ProcessaAmericanas.csv",
    "ProcessaMesa.csv",
    "ProcessaSemclass.csv",
    "ImpVinhos.csv",
    "ImpEspumantes.csv",
    "ImpFrescas.csv",
    "ImpPassas.csv",
    "ExpVinho.csv",
    "ExpEspumantes.csv",
    "ExpUva.csv",
    "ExpSuco.csv"
}

os.makedirs("dados_embrapa", exist_ok=True)

for nome_arquivo, url in arquivos:
    print(f"Baixando e convertendo {nome_arquivo} ...")
    
    response = requests.get(url)
    if response.status_code == 200:
        csv_string = response.content.decode('utf-8')
        csv_buffer = StringIO(csv_string)
        
        try:
            if nome_arquivo in tsv_arquivos:
                df = pd.read_csv(csv_buffer, sep='\t', on_bad_lines='skip')
                caminho_saida = os.path.join("dados_embrapa", nome_arquivo)
                df.to_csv(caminho_saida, sep='\t', index=False)
                print(f"Salvo como TSV (tabulação) em {caminho_saida}")
            else:
                df = pd.read_csv(csv_buffer, sep=';', on_bad_lines='skip')
                caminho_saida = os.path.join("dados_embrapa", nome_arquivo.replace('.csv', '.xlsx'))
                df.to_excel(caminho_saida, index=False)
                print(f"Salvo como Excel em {caminho_saida}")
        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")
    else:
        print(f"Erro ao baixar {nome_arquivo}: Status {response.status_code}")

print("✅ Todos os arquivos foram baixados e tratados com sucesso!")
