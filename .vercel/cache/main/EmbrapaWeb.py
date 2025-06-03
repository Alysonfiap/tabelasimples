import requests
from bs4 import BeautifulSoup

url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

page = requests.get(url, headers=headers)

print(page.text)
