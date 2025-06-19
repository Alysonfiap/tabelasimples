# 🍇 VitiBrasil Scraper + API

Este projeto realiza a extração automatizada dos dados do site [VitiBrasil/EMBRAPA](http://vitibrasil.cnpuv.embrapa.br/), insere essas informações em um banco de dados SQLite e fornece uma API REST para consulta dos dados estruturados.

## 📌 Objetivos

- Coletar dados históricos do site da embrapa brasileira desde 1970
- Armazenar essas informações em banco SQLite local
- Disponibilizar os dados via API pública para análise e uso em projetos de dados

## 🚀 Documentação da API

A API está hospedada na Vercel com documentação:

🔗 **[Documentação Swagger](https://vitibrasil-api-hlz2-git-master-alysons-projects-f292937b.vercel.app/docs)**

## 🔍 Exemplos de Consulta

- Dados gerais de produção:  
  [`/producao`](https://vitibrasil-api-hlz2-git-master-alysons-projects-f292937b.vercel.app/producao)

- Dados de produção para o ano de 2021:  
  [`/producao/2021`](https://vitibrasil-api-hlz2-git-master-alysons-projects-f292937b.vercel.app/producao/2021)

⚠️ Esses são apenas **exemplos**. A API oferece acesso a outras tabelas como:
- Comercialização (`/comercializacao`)
- Processamento (`/processamento`)
- Importação (`/importacao`)
- Exportação (`/exportacao`)

Todas podem ser consultadas por ano ou integralmente.

## ⚙️ Como funciona o scraper?

O script coleta os dados de forma paralela com `ThreadPoolExecutor` e estrutura os dados com `pandas`, realizando limpeza de colunas e inserção no SQLite.
