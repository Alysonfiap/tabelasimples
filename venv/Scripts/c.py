import requests

url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2021&opcao=opt_02'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

# Salvar o HTML em um arquivo local
with open("pagina_opt03.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("HTML salvo com sucesso.")


