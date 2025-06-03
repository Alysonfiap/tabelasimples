# 📊 Projeto Vitibrasil - Coleta e Consulta de Dados com FastAPI

Este projeto tem como objetivo **automatizar a coleta de dados do site Vitibrasil** e disponibilizar uma **API RESTful** para consultas organizadas e padronizadas usando **FastAPI**.

## 🧠 Visão Geral

O sistema está dividido em duas partes principais:

1. **Coleta de dados via Web Scraping** com `requests`, `BeautifulSoup` e `pandas`
2. **Armazenamento em banco SQLite** e **criação de uma API de consulta com FastAPI**

---
 Rotas da API
🔍 Consulta geral por ano
http
Copiar
Editar
GET /{tabela}/{ano}
Exemplos:
/producao/2020 → Produção daquele ano

/comercializacao/2015 → Comercialização

/processamento/2019 → Processamento de uvas

/importacao/2022 → Importações

/exportacao/2021 → Exportações

🧠 Regras de roteamento
A consulta muda com base no nome da tabela:

Tabela	Campos incluídos na resposta
producao	ano, produto, quantidade_l
comercializacao	ano, produto, quantidade_l
processamento	ano, cultivar, quantidade_kg, sem_definição
importacao	países, quantidade_kg, valor_us$
exportacao	países, quantidade_kg, valor_us$

